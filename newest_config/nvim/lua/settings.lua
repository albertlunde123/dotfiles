g = let
o = set

local g = vim.g
local o = vim.o


vim.api.nvim_command('syntax enable')
vim.api.nvim_command('filetype plugin indent on')
-- o.guifont = 'Hack Nerd Font:h12'
o.termguicolors = true
o.background = 'dark'

-- Do not save when switching buffers
-- o.hidden = true

-- Decrease update time
o.timeoutlen = 500
o.updatetime = 200

-- Number of screen lines to keep above and below the cursor
o.scrolloff = 8

-- Better editor UI
o.number = true
o.numberwidth = 5
o.relativenumber = true
o.signcolumn = 'no'
o.cursorline = false

-- Better editing experience
o.expandtab = true
-- o.smarttab = true
o.cindent = true
o.smartindent = true
o.autoindent = true
o.wrap = true
o.textwidth = 10000
o.tabstop = 4
o.shiftwidth = 0
o.softtabstop = -1 -- If negative, shiftwidth value is used
o.list = true
o.listchars = 'trail:·,nbsp:◇,tab:→ ,extends:▸,precedes:◂'
-- o.listchars = 'eol:¬,space:·,lead: ,trail:·,nbsp:◇,tab:→-,extends:▸,precedes:◂,multispace:···⬝,leadmultispace:│   ,'
-- o.formatoptions = 'qrn1'

-- Makes neovim and host OS clipboard play nicely with each other
o.clipboard = 'unnamedplus'

-- Case insensitive searching UNLESS /C or capital in search
o.ignorecase = true
o.smartcase = true

-- Undo and backup options
o.backup = false
o.writebackup = false
o.undofile = true
o.swapfile = false
-- o.backupdir = '/tmp/'
-- o.directory = '/tmp/'
-- o.undodir = '/tmp/'

-- Remember 50 items in commandline history
o.history = 50

-- Better buffer splitting
o.splitright = true
o.splitbelow = true

-- Preserve view while jumping
o.jumpoptions = 'view'

-- Stable buffer content on window open/close events.
o.splitkeep = 'screen'

-- Improve diff
-- vim.opt.diffopt:append('linematch:60')

-- WARN: this won't update the search count after pressing `n` or `N`
-- When running macros and regexes on a large file, lazy redraw tells neovim/vim not to draw the screen
-- o.lazyredraw = true

-- Better folds (don't fold by default)
-- o.foldmethod = 'indent'
-- o.foldlevelstart = 99
-- o.foldnestmax = 3
-- o.foldminlines = 1

-- spelling
o.spelllang=en_gb

-- Map <leader> to space
g.mapleader = ','
g.maplocalleader = ','

-- disable highlightserach

o.hlsearch = false


------- Things that dont require let.

local M = {}
M.treesitter_ensure_installed = {
  "bash",
  "cmake",
  "css",
  "dockerfile",
  "go",
  "hcl",
  "html",
  "java",
  "javascript",
  "json",
  "kotlin",
  "latex",
  "ledger",
  "lua",
  "markdown",
  "markdown_inline",
  "query",
  "python",
  "regex",
  "r",
  "toml",
  "vim",
  "yaml",
}

return M
