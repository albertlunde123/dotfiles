-- for the file ~/.config/i3/config set fileype to i3config
vim.cmd([[
augroup filetypedetect
  autocmd!
  au BufRead,BufNewFile ~/.config/i3/config set filetype=i3config
  au BufRead,BufNewFile ~/.i3/config set filetype=i3config
augroup END
]])
