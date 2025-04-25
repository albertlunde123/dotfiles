require('plugins')
require('settings')
require('keybindings')
require('autocommands')
require('todo')
-- require('i3')
-- require('functions')
require('floating_window')


vim.o.background = "dark" --
--
function save_as_root()
  current_file = vim.api.nvim_buf_get_name(0)
  vim.api.nvim_command('write !SUDO_ASKPASS=/home/albert/.config/nvim/lua/askpass.sh sudo -A tee ' .. current_file .. ' >/dev/null')
  vim.api.nvim_command('edit!') -- Reload the file to update any changes made by sudo
end

-- Keybinding: <Leader>rs to save the current file as root
vim.api.nvim_set_keymap('n', '<Leader>su', ':lua save_as_root()<CR>', {noremap = true, silent = true})


vim.cmd([[
  " Open NERDTree in the current file's directory
  command! NERDTreeCWD :exec 'NERDTree' expand('%:p:h')
]])

-- Put this in your init.lua or a separate Lua file

-- Lua function to write selection to file
--
function write_selection_to_file()
  -- Get the start and end of the visual selection
  local line_start, column_start = unpack(vim.fn.getpos("'<"), 2)
  local line_end, column_end = unpack(vim.fn.getpos("'>"), 2)

  -- Get the lines in the visual selection
  local lines = vim.fn.getline(line_start, line_end)

  -- Adjust the first and last line to match the visual selection
  lines[1] = string.sub(lines[1], column_start)
  lines[#lines] = string.sub(lines[#lines], 1, column_end)

  -- Write the lines to the file
  local filename = "/home/albert/.config/nvim/selection.txt"
  vim.fn.writefile(lines, filename)
  vim.fn.printf("Wrote %d lines to %s", #lines, filename)
  vim.fn.system("python3 ~/.config/nvim/GPT4/code_suggestion.py")

  
  open_floating_window()
  
end


function MagmaInitPython()
    vim.cmd[[
    :MagmaInit python
    :MagmaEvaluateArgument a=5
    ]]
end
vim.api.nvim_set_keymap('v', '<leader>w', ':<C-u>lua write_selection_to_file()<CR>', {noremap = true, silent = true})

