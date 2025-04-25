require("functions")

local function map(m, k, v)
	vim.keymap.set(m, k, v, {silent = true})
end

------------------------------------------------
-- normal mode bindings
-- jump to end of line,
-- jump to start of line
-- jump between windows

map('n', 'L', '$')
map('n', 'H', '0')
map('n', 'gg', 'ggzz')
map('n', 'G', 'Gzz')
map('i', 'jk', '<Esc>')
map('v', 'jk', '<Esc>')

-- yank end of line
map('n', 'yL', 'y$')
-- reload nvim
map('n', '<leader>rs', ':luafile %<CR>')

-- Move around between windows
map('n', '<C-j>', '<C-w>j')
map('n', '<C-h>', '<C-w>h')
map('n', '<C-k>', '<C-w>k')
map('n', '<C-l>', '<C-w>l')

-- Move windows around
map('n', ',<C-J>', '<C-w>J')
map('n', ',<C-H>', '<C-w>H')
map('n', ',<C-K>', '<C-w>K')
map('n', ',<C-L>', '<C-w>L')

-- Add blank line
map('n', '<C-o>', 'o<Esc>')
map('n', 'DD', 'ddk')

-- Leap up and down at a greater pace
map('n', '<C-D>', '10j')
map('n', '<C-F>', '10k')
--- remove highlight
map('n', '<leader>h', ':noh<CR>')
map('n', '<leader>w', ':w<CR>')
map('n', '<leader>q', ':wq<CR>')
map('n', '<leader>Q', ':q!<CR>')

---------------------------------
---- open NERDTree

map('n', '<C-n>', ':NvimTreeOpen<CR>')

------------------------------------------------
-- Kør makroer hurtigt
map('n', '<Space>', '@q')
map('n', '<leader>a', '@a')

-- Center buffer

map('n', '<leader>z', "<cmd>lua require'centerpad'.toggle{ leftpad = 20, rightpad = 20 }<cr>", { silent = true, noremap = true })

------------------------------------------------
-- Luk terminal vinduer med 
vim.api.nvim_set_keymap("t", "q", ":q<CR>:bdelete<CR>", {noremap = true})
------------------------------------------------
-- One-eyed kirby
map('c', '<leader>l', "\\(.*\\)", {noremap = true})
map('n', '<leader>f', ':Telescope find_files<CR>', {noremap = true})

--- Resize splits

map('n', '<C-Up>', ':resize -2<CR>')
map('n', '<C-Down>', ':resize +2<CR>')
map('n', '<C-Left>', ':vertical resize -2<CR>')
map('n', '<C-Right>', ':vertical resize +2<CR>')

map('v', '<leader>w', ':call WriteSelectionToFile()<CR>', {noremap = true, silent = true})


vim.api.nvim_set_keymap("n", "<leader>ur", ":UpdateRemotePlugins <bar> lua vim.cmd('silent! restart')<CR>", {noremap = true, silent = true})

map('n', '<leader>s', ']s', {noremap = true, silent = true})

-- Remove trailing whitespaces
function remove_eol_whitespace()
  local start_line = 1
  local end_line = vim.fn.line('$')
  for line_num = start_line, end_line do
    local line = vim.fn.getline(line_num)
    local trimmed_line = string.gsub(line, "%s+$", "")
    if line ~= trimmed_line then
      vim.fn.setline(line_num, trimmed_line)
    end
  end
end

-- Keybinding to trigger the function
vim.api.nvim_set_keymap('n', '<leader>rw', [[<Cmd>lua remove_eol_whitespace()<CR>]], { noremap = true, silent = true })

map("n", "gD",  vim.lsp.buf.definition)
map("n", "K",  vim.lsp.buf.hover)
map("n", "gi", vim.lsp.buf.implementation)
map("n", "gr", vim.lsp.buf.references)
map("n", "gds", vim.lsp.buf.document_symbol)
map("n", "gws", vim.lsp.buf.workspace_symbol)
map("n", "<leader>cl", vim.lsp.codelens.run)
map("n", "<leader>sh", vim.lsp.buf.signature_help)
map("n", "<leader>rn", vim.lsp.buf.rename)
map("n", "<leader>f", vim.lsp.buf.format)
map("n", "<leader>ca", vim.lsp.buf.code_action)


