local A = vim.api

A.nvim_create_autocmd('BufWritePost', {
    group = vim.api.nvim_create_augroup('PACKER', { clear = true }),
    pattern = 'plugins.lua',
    command = 'source <afile> | PackerCompile',
})

local function get_config(name)
  return string.format('require("config.%s")', name)
end

return require('packer').startup({
    function(use)
        ---------------------
        -- Package Manager --
        ---------------------

        use('wbthomason/packer.nvim')
--install telescope.nvim
        --

     -- Toggle Term
        -- Added this plugin.
        use({
            'akinsho/toggleterm.nvim',
            tag = "*",
            config = get_config('toggleterm')
            -- config = true
        })
        -- Telescope
        use({
            'nvim-telescope/telescope.nvim',
            tag  = '0.1.0', 
            config = get_config('telescope'),
            requires = {
                'nvim-lua/popup.nvim' ,
                'nvim-lua/plenary.nvim' ,
                'nvim-telescope/telescope-fzf-native.nvim', run = 'make' }
        })
        ----------------------
        -- Required plugins --
        ----------------------

        use('nvim-lua/plenary.nvim')


        use({
            '~/.config/nvim/plugin-gpt4',
        })
        ----------------------
        -- File Tree ---------
        ----------------------

        use('preservim/nerdtree')

        ----------------------
        -- Github Copilot ----
        ----------------------

        use('github/copilot.vim')

        ----------------------
        -- Movement ----------
        ----------------------

        use('tpope/vim-commentary')
        use('tpope/vim-surround')

        ----------------------
        -- Python ------------
        ----------------------

        -- use('vim-scripts/indentpython.vim')
        -- Plug 'python-mode/python-mode', { 'for': 'python', 'branch': 'develop' }
        --     "let g:pymode_rope = 0
        --     "let g:pymode_rope_completion = 0
        --     "let g:pymode_rope_completion_bind = '<C-Space>'
        --     "let g:pymode_rope_complete_on_dot = 0
        -- use('vim-python/python-syntax')

        -------------------------
        -- syntax highlighting --
        -------------------------

        use({
           "nvim-treesitter/nvim-treesitter",
            config = get_config("treesitter"),
            requires = {"latex-lsp/tree-sitter-latex"},
            -- run = ":TSUpdate",
        })
        use('sheerun/vim-polyglot')
        -- use({
        --     'quarto-dev/quarto-nvim',
        --     config = get_config("quarto-nvim"),
        --     requires = {'neovim/nvim-lspconfig'}
        -- })

        -------------------------
        -- Latex ----------------
        -------------------------

        use({
            'lervag/vimtex',
            config = [[require("config.vimtex")]]
        })

        -------------------------
        ----- Pywal -------------
        -------------------------
        -- use({'AlphaTechnolog/pywal.nvim',
        --     config = get_config("pywal"),
        --     as = 'pywal' })
        use({'folke/tokyonight.nvim',
            config = get_config("tokyonight")})
        -- use { "ellisonleao/gruvbox.nvim" }
        -------------------------
        ------ Lightline --------
        -------------------------
        use({'nvim-lualine/lualine.nvim',
            config = get_config("lualine"),
            requires = { 'kyazdani42/nvim-web-devicons', opt = true }
            })

        -------------------------
        ------ Ultisnips --------
        -------------------------
        use({'sirver/ultisnips',
            config = [[require("config.ultisnips")]]
            })
        -------------------------
        ---- Indent viewer ------
        -------------------------
        use({"lukas-reineke/indent-blankline.nvim",
            config = get_config("indent-blankline")
            })
        -------------------------
        ---- Autocompletion -----
        -------------------------
        use({'hrsh7th/nvim-cmp',
            config = get_config("nvim-cmp"),
            requires = { 'hrsh7th/cmp-nvim-lsp',
                        'hrsh7th/cmp-buffer',
                        'hrsh7th/cmp-path',
                        'neovim/nvim-lspconfig',
                        'hrsh7th/cmp-cmdline',
                        'hrsh7th/nvim-cmp',
                        'quangnguyen30192/cmp-nvim-ultisnips'}
            })
        -------------------------
        ------- Colorizer -------
        -------------------------
        use({'norcalli/nvim-colorizer.lua',
            config = get_config("colorizer")})
        -------------------------
        ------- CSV-files -------
        -------------------------

        use({'smithbm2316/centerpad.nvim'})
    end})

