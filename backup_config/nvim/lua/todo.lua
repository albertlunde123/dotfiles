function set_todo_input_options()
  vim.api.nvim_command("startinsert")
  vim.api.nvim_command("setlocal nolist nonumber norelativenumber")
  vim.api.nvim_command("setlocal laststatus=0")
  vim.api.nvim_command("setlocal nocursorline")
  vim.api.nvim_command("setlocal nocursorcolumn")
  vim.api.nvim_command("setlocal nofoldenable")
  vim.api.nvim_command("setlocal noshowcmd noshowmode")
  require('cmp').setup.buffer {enabled = false}
end

function set_todo_input_mappings()
  vim.api.nvim_command("inoremap <CR> <Esc>:w<CR>:q<CR>")
end

vim.api.nvim_command("au BufRead,BufNewFile ../../../tmp/todo_input.txt lua vim.api.nvim_buf_set_option(vim.api.nvim_get_current_buf(), 'filetype', 'todo_input')")
-- vim.api.nvim_command("autocmd VimLeave * lua vim.api.nvim_command('silent !kitty -class ''todo_input'' quit')")
vim.api.nvim_command("autocmd FileType todo_input lua set_todo_input_options()")
vim.api.nvim_command("autocmd FileType todo_input lua set_todo_input_mappings()")

