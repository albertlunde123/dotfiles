" nvim_temp_config.vim

set nonumber
set laststatus=0
set noswapfile
set fillchars=eob:\ ,vert:\│,fold:\ ,diff:\ ,msgsep:‾ 

highlight Normal ctermbg=NONE guibg=NONE
highlight NonText ctermbg=NONE guibg=NONE

inoremap <buffer> <CR> <Esc>:wq<CR>
startinsert
