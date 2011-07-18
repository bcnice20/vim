set nocompatible
set hidden

syntax on
colorscheme blazer
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

inoremap <expr> <CR> pumvisible() ? "\<C-y>" : "\<C-g>u\<CR>"
inoremap <expr> <C-n> pumvisible() ? '<C-n>' :
  \ '<C-n><C-r>=pumvisible() ? "\<lt>Down>" : ""<CR>'

inoremap <expr> <M-,> pumvisible() ? '<C-n>' :
  \ '<C-x><C-o><C-n><C-p><C-r>=pumvisible() ? "\<lt>Down>" : ""<CR>'

let mapleader = ","
let g:mapleader = ","

" Fast saving
nmap <leader>w :w!<cr>

" Fast editing of the .vimrc
map <leader>e :e! ~/.vimrc<cr>

nmap <leader>o <C-x><C-o><cr>
command! FR set filetype=ruby

set gfn=Monospace\ bold\ 12
set guioptions-=m
set guioptions-=T
set guioptions-=r
set nobackup
set noswapfile
set history=1000
set undolevels=1000
set ruler		" show the cursor position all the time
set showcmd		" display incomplete commands
map Q gq

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


"""Fuzzy Finder"""
nmap ff :FufFile<CR> 
nmap fb :FufBuffer<CR>
nmap fd :FufDir<CR>
nmap fl :FufLine<CR>

""""NerdTree""""
nmap nt :NERDTreeToggle<CR>

let g:BASH_AuthorName ='Brad Carter'
let g:BASH_Email ='bcnice20@gmail.com'
let g:BASH_Company ='thebcblends'

" Really useful!
"  In visual mode when you press * or # to search for the current selection
vnoremap <silent> * :call VisualSearch('f')<CR>
vnoremap <silent> # :call VisualSearch('b')<CR>

" When you press gv you vimgrep after the selected text
vnoremap <silent> gv :call VisualSearch('gv')<CR>
map <leader>g :vimgrep // **/*.<left><left><left><left><left><left><left>

cno $h e ~/
cno $d e ~/Desktop/
cno $j e ./
cno $c e <C-\>eCurrentFileDir("e")<cr>

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

" omnicompletion menu colors
hi Pmenu cterm=none ctermfg=Green ctermbg=none
hi PmenuSel cterm=underline ctermfg=White ctermbg=none
hi PmenuSbar cterm=bold ctermfg=none ctermbg=DarkBlue
hi PmenuThumb cterm=bold ctermfg=none ctermbg=White
