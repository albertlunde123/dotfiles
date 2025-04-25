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
        --

     -- Toggle Term
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
        --------------------
        ---

        use('nvim-lua/plenary.nvim')

        ----------------------
        -- File Tree ---------
        ----------------------

        use({
            'kyazdani42/nvim-tree.lua',
            config = get_config('nvim-tree'),
            requires = 'kyazdani42/nvim-web-devicons'
        })
        ----------------------
        -- Github Copilot ----
        ----------------------

        -- use('github/copilot.vim')

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
            'nvim-treesitter/nvim-treesitter',
            run = ':TSUpdate', -- Automatically update parsers
            config = function()
                require('nvim-treesitter.configs').setup({
                    ensure_installed = { -- List of languages to install parsers for
                        "lua", "python", "javascript", "html", "css", "bash", "json", "markdown", "latex", "scala"
                    },
                    highlight = {
                        enable = true, -- Enable syntax highlighting
                        disable = {"latex"},
                        additional_vim_regex_highlighting = false, -- Disable Vim's regex-based highlighting
                    },
                    indent = {
                        enable = true, -- Enable tree-sitter-based indentation
                    },
                })
            end,
        })

        -------------------------
        ----- LSP ---------------
        -------------------------

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
        use({'AlphaTechnolog/pywal.nvim',
            config = get_config("pywal"),
            as = 'pywal' })

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

