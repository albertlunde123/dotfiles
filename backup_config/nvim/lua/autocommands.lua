local A = vim.api
local num_au = A.nvim_create_augroup('NUMTOSTR', { clear = true })

-- Highlight the region on yank
A.nvim_create_autocmd('TextYankPost', {
    group = num_au,
    callback = function()
        vim.highlight.on_yank({ higroup = 'Visual' })
        -- This is a workaround for clipboard not working in WSL
        -- see https://github.com/neovim/neovim/issues/19204#issuecomment-1173722375
        -- if vim.fn.has('wsl') == 1 then
        --     vim.fn.system('clip.exe', vim.fn.getreg('"'))
        -- end
    end,
})

local leader = "<leader>"
function on_python_filetype()
  -- Set up a mapping for the `ll` command
  vim.api.nvim_set_keymap("n", leader .. "ll", [[
    :w<CR>:split term://python3 %<CR>a
  ]], {noremap = true})
end

-- Register the function as a handler for the "FileType" event
A.nvim_command("autocmd FileType python lua on_python_filetype()")

-- Setup som latex-keybindings
function on_latex_filetype()
    vim.api.nvim_set_keymap("n", leader .. "ll", [[:w<CR>:VimtexCompile<CR>]], {noremap = true})
    vim.api.nvim_set_keymap("n", leader .. "lv", [[:w<CR>:VimtexView<CR>]], {noremap = true})
    vim.api.nvim_set_keymap("i", "<C-f>", [[<Esc>: silent exec '.!inkscape-figures create "'.getline('.').'" "'.b:vimtex.root.'/figures/"'<CR><CR>:w<CR>]], {noremap = true})
    vim.api.nvim_set_keymap("n", leader .. 'u', [[:w<CR>:split<CR> :UltiSnipsEdit<CR>]], {noremap = true})
    vim.api.nvim_set_keymap("n", "<C-f>", [[: silent exec '!inkscape-figures edit "'.b:vimtex.root.'/figures/" > /dev/null 2>&1 &'<CR><CR>:redraw!<CR>]], {noremap = true})
end

A.nvim_command("autocmd FileType tex lua on_latex_filetype()")

-- windows to close with "q"
A.nvim_create_autocmd(
  "FileType",
  { pattern = { "help", "startuptime", "qf", "lspinfo" }, command = [[nnoremap <buffer><silent> q :close<CR>]] }
)

A.nvim_create_autocmd("FileType", { pattern = "man", command = [[nnoremap <buffer><silent> q :quit<CR>]] })


-- open pdfs with zathura, close the vim window
A.nvim_create_autocmd(
  "FileType",
  { pattern = "pdf", command = [[nnoremap <buffer><silent> q :silent !zathura %<CR>:close<CR>]] }
)
