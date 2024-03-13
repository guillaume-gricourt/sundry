syntax on
set ruler

set encoding=utf-8

"set textwidth=80
set tabstop=4
set softtabstop=4
set expandtab
set shiftwidth=4
set autoindent

highlight RedundantSpaces ctermbg=red guibg=red
match RedundantSpaces /\s\+$/
set backspace=indent,eol,start

" Pluging manager: https://github.com/junegunn/vim-plug
call plug#begin('~/.vim/plugged')
Plug 'snakemake/snakefmt'
Plug 'snakemake/snakemake', {'rtp':'misc/vim'}
Plug 'psf/black', {'branch': 'stable'}
Plug 'fisadev/vim-isort'
Plug 'rhysd/vim-clang-format'
call plug#end()

" Snakemake
au BufNewFile,BufRead Snakefile,*.smk set filetype=snakemake
au FileType snakemake autocmd BufWritePre <buffer> execute ':Snakefmt'

" JS - Prettier
packloadall
let g:prettier#autoformat = 1
let g:prettier#autoformat_require_pragma = 0

" Python - Black
let g:black_virtualenv="~/.vim/vim_black"
augroup black_on_save
  autocmd!
  autocmd BufWritePre *.py Black
augroup end

" Python - Isort
" let g:vim_isort_map = '<C-i>'
augroup isort_on_save
  autocmd!
  autocmd BufWritePre *.py Isort
augroup end

" Clang Format
let g:clang_format#style_options = {
            \ "AccessModifierOffset" : -4,
            \ "AllowShortIfStatementsOnASingleLine" : "true",
            \ "AlwaysBreakTemplateDeclarations" : "true",
            \ "Standard" : "C++11"}
autocmd FileType c,cpp ClangFormatAutoEnable
