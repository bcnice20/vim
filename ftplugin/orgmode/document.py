# -*- coding: utf-8 -*-

from exceptions import BufferNotFound, BufferNotInSync
from liborgmode import Document, Heading, MultiPurposeList, DIRECTION_BACKWARD
import settings
import vim
from UserList import UserList

class VimBufferContent(MultiPurposeList):
	u""" Vim Buffer Content is a UTF-8 wrapper around a vim buffer. When
	retrieving or setting items in the buffer an automatic conversion is
	performed.

	This ensures UTF-8 usage on the side of liborgmode and the vim plugin
	vim-orgmode.
	"""

	def __init__(self, vimbuffer, on_change=None):
		MultiPurposeList.__init__(self, on_change=on_change)

		# replace data with vimbuffer to make operations change the actual
		# buffer
		self.data = vimbuffer

	def __contains__(self, item):
		i = item
		if type(i) is unicode:
			i = item.encode(u'utf-8')
		return MultiPurposeList.__contains__(self, i)

	def __getitem__(self, i):
		item = MultiPurposeList.__getitem__(self, i)
		if type(item) is str:
			return item.decode(u'utf-8')
		return item

	def __getslice__(self, i, j):
		return [item.decode(u'utf-8') if type(item) is str else item \
				for item in MultiPurposeList.__getslice__(self, i, j)]

	def __setitem__(self, i, item):
		_i = item
		if type(_i) is unicode:
			_i = item.encode(u'utf-8')

		MultiPurposeList.__setitem__(self, i, _i)

	def __setslice__(self, i, j, other):
		o = []
		o_tmp = other
		if type(o_tmp) not in (list, tuple) and not isinstance(o_tmp, UserList):
			o_tmp = list(o_tmp)
		for item in o_tmp:
			if type(item) == unicode:
				o.append(item.encode(u'utf-8'))
			else:
				o.append(item)
		MultiPurposeList.__setslice__(self, i, j, o)

	def __add__(self, other):
		raise NotImplementedError()
		# TODO: implement me
		if isinstance(other, UserList):
			return self.__class__(self.data + other.data)
		elif isinstance(other, type(self.data)):
			return self.__class__(self.data + other)
		else:
			return self.__class__(self.data + list(other))

	def __radd__(self, other):
		raise NotImplementedError()
		# TODO: implement me
		if isinstance(other, UserList):
			return self.__class__(other.data + self.data)
		elif isinstance(other, type(self.data)):
			return self.__class__(other + self.data)
		else:
			return self.__class__(list(other) + self.data)

	def __iadd__(self, other):
		o = []
		o_tmp = other
		if type(o_tmp) not in (list, tuple) and not isinstance(o_tmp, UserList):
			o_tmp = list(o_tmp)
		for i in o_tmp:
			if type(i) is unicode:
				o.append(i.encode(u'utf-8'))
			else:
				o.append(i)

		return MultiPurposeList.__iadd__(self, o)

	def append(self, item):
		i = item
		if type(item) is str:
			i = item.encode(u'utf-8')
		MultiPurposeList.append(self, i)

	def insert(self, i, item):
		_i = item
		if type(_i) is str:
			_i = item.encode(u'utf-8')
		MultiPurposeList.insert(self, i, _i)

	def index(self, item, *args):
		i = item
		if type(i) is unicode:
			i = item.encode(u'utf-8')
		MultiPurposeList.index(self, i, *args)

	def pop(self, i=-1):
		return MultiPurposeList.pop(self, i).decode(u'utf-8')

	def extend(self, other):
		o = []
		o_tmp = other
		if type(o_tmp) not in (list, tuple) and not isinstance(o_tmp, UserList):
			o_tmp = list(o_tmp)
		for i in o_tmp:
			if type(i) is unicode:
				o.append(i.encode(u'utf-8'))
			else:
				o.append(i)
		MultiPurposeList.extend(self, o)

class VimBuffer(Document):
	def __init__(self, bufnr=0):
		u"""
		:bufnr:		0: current buffer, every other number refers to another buffer
		"""
		Document.__init__(self)
		self._bufnr            = vim.current.buffer.number if bufnr == 0 else bufnr
		self._changedtick      = -1

		if self._bufnr == vim.current.buffer.number:
			self._content = VimBufferContent(vim.current.buffer)
		else:
			_buffer = None
			for b in vim.buffers:
				if self._bufnr == b.number:
					_buffer = b
					break

			if not _buffer:
				raise BufferNotFound(u'Unable to locate buffer number #%d' % self._bufnr)
			self._content = VimBufferContent(_buffer)

		self.update_changedtick()
		self._orig_changedtick = self._changedtick

	@property
	def tabstop(self):
		return int(vim.eval(u'&ts'.encode(u'utf-8')))

	@property
	def tag_column(self):
		return int(settings.get('org_tag_column', '77'))

	@property
	def is_insync(self):
		if self._changedtick == self._orig_changedtick:
			self.update_changedtick()
		return self._changedtick == self._orig_changedtick

	@property
	def bufnr(self):
		u"""
		:returns:	The buffer's number for the current document
		"""
		return self._bufnr

	def changedtick():
		""" Number of changes in vimbuffer """
		def fget(self):
			return self._changedtick
		def fset(self, value):
			self._changedtick = value
		return locals()
	changedtick = property(**changedtick())

	def update_changedtick(self):
		if self.bufnr == vim.current.buffer.number:
			self._changedtick = int(vim.eval(u'b:changedtick'.encode(u'utf-8')))
		else:
			vim.command(u'unlet! g:org_changedtick | let g:org_lz = &lz | let g:org_hidden = &hidden | set lz hidden'.encode(u'utf-8'))
			# TODO is this likely to fail? maybe some error hangling should be added
			vim.command((u'keepalt buffer %d | let g:org_changedtick = b:changedtick | buffer %d' % \
					(self.bufnr, vim.current.buffer.number)).encode(u'utf-8'))
			vim.command(u'let &lz = g:org_lz | let &hidden = g:org_hidden | unlet! g:org_lz g:org_hidden | redraw'.encode(u'utf-8'))
			self._changedtick = int(vim.eval(u'g:org_changedtick'.encode(u'utf-8')))

	def write(self):
		u""" write the changes to the vim buffer

		:returns:	True if something was written, otherwise False
		"""
		if not self.is_dirty:
			return False

		self.update_changedtick()
		if not self.is_insync:
			raise BufferNotInSync(u'Buffer is not in sync with vim!')

		# write meta information
		if self.is_dirty_meta_information:
			meta_end = 0 if self._orig_meta_information_len is None else self._orig_meta_information_len
			self._content[:meta_end] = self.meta_information
			self._orig_meta_information_len = len(self.meta_information)

		# remove deleted headings
		already_deleted = []
		for h in sorted(self._deleted_headings, cmp=lambda x, y: cmp(x._orig_start, y._orig_start), reverse=True):
			if h._orig_start is not None and h._orig_start not in already_deleted:
				# this is a heading that actually exists on the buffer and it
				# needs to be removed
				del self._content[h._orig_start:h._orig_start + h._orig_len]
				already_deleted.append(h._orig_start)
		del self._deleted_headings[:]
		del already_deleted

		# update changed headings and add new headings
		for h in self.all_headings():
			if h.is_dirty:
				if h._orig_start is not None:
					# this is a heading that existed before and was changed. It
					# needs to be replaced
					if h.is_dirty_heading:
						self._content[h.start:h.start + 1] = [unicode(h)]
					if h.is_dirty_body:
						self._content[h.start + 1:h.start + h._orig_len] = h.body
				else:
					# this is a new heading. It needs to be inserted
					self._content[h.start:h.start] = [unicode(h)] + h.body
				h._dirty_heading = False
				h._dirty_body = False
			# for all headings the length and start offset needs to be updated
			h._orig_start = h.start
			h._orig_len = len(h)

		self._dirty_meta_information = False
		self._dirty_document = False

		self.update_changedtick()
		self._orig_changedtick = self._changedtick
		return True

	def write_heading(self, heading, including_children=True):
		""" WARNING: use this function only when you know what you are doing!
		This function writes a heading to the vim buffer. It offers performance
		advantages over the regular write() function. This advantage is
		combined with no sanity checks! Whenever you use this function, make
		sure the heading you are writing contains the right offsets
		(Heading._orig_start, Heading._orig_len).

		Usage example:
			# Retrieve a potentially dirty document
			d = ORGMODE.get_document(allow_dirty=True)
			# Don't rely on the DOM, retrieve the heading afresh
			h = d.find_heading(direction=DIRECTION_FORWARD, position=100)
			# Update tags
			h.tags = ['tag1', 'tag2']
			# Write the heading
			d.write_heading(h)

		This function can't be used to delete a heading!

		:heading:				Write this heading with to the vim buffer
		:including_children:	Also include children in the update

		:returns				The written heading
		"""
		if including_children and heading.children:
			for child in heading.children[::-1]:
				self.write_heading(child, including_children)

		if heading.is_dirty:
			if heading._orig_start is not None:
				# this is a heading that existed before and was changed. It
				# needs to be replaced
				if heading.is_dirty_heading:
					self._content[heading._orig_start:heading._orig_start + 1] = [unicode(heading)]
				if heading.is_dirty_body:
					self._content[heading._orig_start + 1:heading._orig_start + heading._orig_len] = heading.body
			else:
				# this is a new heading. It needs to be inserted
				raise ValueError('Heading must contain the attribute _orig_start! %s' % heading)
			heading._dirty_heading = False
			heading._dirty_body = False
		# for all headings the length offset needs to be updated
		heading._orig_len = len(heading)

		return heading

	def previous_heading(self, position=None):
		u""" Find the next heading (search forward) and return the related object
		:returns:	 Heading object or None
		"""
		h = self.current_heading(position=position)
		if h:
			return h.previous_heading

	def current_heading(self, position=None):
		u""" Find the current heading (search backward) and return the related object
		:returns:	Heading object or None
		"""
		if position is None:
			position = vim.current.window.cursor[0] - 1
		for h in self.all_headings():
			if h.start <= position and h.end >= position:
				return h

	def next_heading(self, position=None):
		u""" Find the next heading (search forward) and return the related object
		:returns:	 Heading object or None
		"""
		h = self.current_heading(position=position)
		if h:
			return h.next_heading

	def find_current_heading(self, position=None, heading=Heading):
		u""" Find the next heading backwards from the position of the cursor.
		The difference to the function current_heading is that the returned
		object is not built into the DOM. In case the DOM doesn't exist or is
		out of sync this function is much faster in fetching the current
		heading.

		:position:	The position to start the search from

		:heading:	The base class for the returned heading

		:returns:	 Heading object or None
		"""
		return self.find_heading(vim.current.window.cursor[0] - 1 \
				if position is None else position, \
				direction=DIRECTION_BACKWARD, heading=heading, \
				connect_with_document=False)
