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
--
map('n', '<C-Q>', '<CMD>q<CR>')

--- remove highlight
map('n', '<leader>h', ':noh<CR>')

---------------------------------
---- open NERDTree

map('n', '<C-n>', ':NERDTree<CR>')

------------------------------------------------
-- Kør makroer hurtigt
map('n', '<Space>', '@q')

---------------------------
---- source init.lua
map('n', '<leader>s', ':source ~/.config/nvim/init.lua<CR>')

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
