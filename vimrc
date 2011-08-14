set nocompatible
set hidden

syntax on
colorscheme herald
set background=dark

filetype plugin on
filetype plugin indent on

set ofu=syntaxcomplete#Complete
let Omnifunc_GlobalScopeSearch   = 1
let Omnifunc_DisplayMode         = 1
let Omnifunc_ShowPrototypeInAbbr = 1 "show prototype in pop-up
let Omnifunc_ShowAccess          = 1 "show access in pop-up
let Omnifunc_SelectFirstItem     = 1 "select first item in pop-up
set completeopt=menuone,menu,longest

let mapleader = "'"
nnoremap ; :

" Fast saving
nmap <leader>w :w!<cr>

" Fast editing of the .vimrc
map <leader>e :e! ~/.vimrc<cr>

set gfn=Monospace\ bold\ 12
set guioptions-=T
set guioptions-=r
set nobackup
set noswapfile
set history=1000
set undolevels=1000
set ruler		" show the cursor position all the time
set showcmd		" display incomplete commands

set mouse=a
set cmdheight=2
set wildmenu
set magic
set nowb
set autoread

try
    if MySys() == "windows"
      set undodir=C:\Windows\Temp
    else
      set undodir=~/.vim_runtime/undodir
    endif

    set undofile
catch
endtry

set softtabstop=2
set nowrap        " don't wrap lines
set tabstop=2     " a tab is two spaces
set backspace=indent,eol,start
                  " allow backspacing over everything in insert mode
set autoindent    " always set autoindenting on
set copyindent    " copy the previous indentation on autoindenting
set number        " always show line numbers
set shiftwidth=2  " number of spaces to use for autoindenting
set shiftround    " use multiple of shiftwidth when indenting with '<' and '>'
set showmatch     " set show matching parenthesis
set ignorecase    " ignore case when searching
set smartcase     " ignore case if search pattern is all lowercase,
                  "    case-sensitive otherwise
set smarttab      " insert tabs on the start of a line according to
                  "    shiftwidth, not tabstop
set hlsearch      " highlight search terms
set incsearch     " show search matches as you type

map<leader>s :shell<CR>

"""Python stuff"""
let python_highlight_all = 1
let ruby_highlight_all = 1

"""Fuzzy Finder"""
map <leader>ff :FufFile<CR> 
map <leader>fb :FufBuffer<CR>
map <leader>fd :FufDir<CR>
map <leader>fl :FufLine<CR>

"""Fuzzy Textmate"""
map <leader>t :FuzzyFinderTextMate<CR>

""""NerdTree""""
nmap nt :NERDTreeToggle<CR>

nmap <leader>md :%!Markdown.pl --html5tags <cr>

" Really useful!
"  In visual mode when you press * or # to search for the current selection
vnoremap <silent> * :call VisualSearch('f')<CR>
vnoremap <silent> # :call VisualSearch('b')<CR>

" When you press gv you vimgrep after the selected text
vnoremap <silent> gv :call VisualSearch('gv')<CR>
map <leader>g :vimgrep // **/*.<left><left><left><left><left><left><left>

" Tab configuration
map tn :tabnew<cr>
map te :tabedit
map tc :tabclose<cr>
map tm :tabmove

"Quickly open a buffer for scripbble
map <leader>q :e ~/buffer<cr>
au BufRead,BufNewFile ~/buffer iab <buffer> xh1 ===========================================

map <leader>pp :setlocal paste!<cr>

"{{{ status line
set laststatus=2
set statusline=
set statusline+=%-10.3n
set statusline+=%f\ " file name
set statusline+=%h%1*%m%r%w%0* " flag
set statusline+=[
set statusline+=%{&fileformat}] " file format
if filereadable(expand("~/.vim/plugin/vimbuddy.vim"))
    set statusline+=\ %{VimBuddy()} " vim buddy
endif
set statusline+=%= " right align
"set statusline+=%2*0x%-8B\ " current char
"set statusline+=0x%-8B\ " current char
set statusline+=%-10.(%l,%c%V%)\ \%L\ %<%P " offset
"}}}

