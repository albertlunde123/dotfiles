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
-- function on_python_filetype()
--   -- Set up a mapping for the `ll` command
--     vim.api.nvim_set_keymap("n", leader .. "ll", [[:w<CR>:split term://python3 %<CR>a]], {noremap = true, silent = true})
-- end

function on_python_filetype()
    vim.api.nvim_set_keymap("n", vim.g.mapleader .. "ll", ":w<CR>" .. ":lua run_in_term()<CR>", {noremap = true, silent = true})
end

function on_txt_filetype()
    -- disable copilot
    A.nvim_command("autocmd FileType txt Copilot disable")
end

function run_in_term()
    local term_found = false
    local term_buf = nil
    local current_win = vim.api.nvim_get_current_win()
    vim.api.nvim_exec([[
        let g:term_win_id = 0
        let g:term_buf_id = 0
        windo if &buftype == 'terminal' | let g:term_win_id = win_getid() | let g:term_buf_id = winbufnr(0) | endif
        ]], false)
    term_buf = vim.api.nvim_get_var('term_buf_id')
    if term_buf ~= 0 then
        term_found = true
    end
    if term_found then
        vim.api.nvim_command("quit")
    end
    vim.api.nvim_command("split term://python3 " .. vim.fn.expand('%:p'))
    vim.api.nvim_set_current_win(current_win)
end
-- Register the function as a handler for the "FileType" event
A.nvim_command("autocmd FileType python lua on_python_filetype()")
A.nvim_command("autocmd BufNewFile *.py lua on_python_filetype()")
A.nvim_command("autocmd FileType txt lua on_txt_filetype()")

-- Setup som latex-keybindings
function on_latex_filetype()
    vim.api.nvim_set_keymap("n", leader .. "ll", [[:w<CR>:VimtexCompile<CR>]], {noremap = true})
    vim.api.nvim_set_keymap("n", leader .. "lv", [[:w<CR>:VimtexView<CR>]], {noremap = true})
    vim.api.nvim_set_keymap("i", "<C-f>", [[<Esc>: silent exec '.!inkscape-figures create "'.getline('.').'" "'.b:vimtex.root.'/figures/"'<CR><CR>:w<CR>]], {noremap = true})
    vim.api.nvim_set_keymap("n", leader .. 'u', [[:w<CR>:split<CR> :UltiSnipsEdit<CR>]], {noremap = true})
    vim.api.nvim_set_keymap("n", "<C-f>", [[: silent exec '!inkscape-figures edit "'.b:vimtex.root.'/figures/" > /dev/null 2>&1 &'<CR><CR>:redraw!<CR>]], {noremap = true})
end

-- disable copilot on latex filetype
A.nvim_command("autocmd FileType tex Copilot disable")

A.nvim_command("autocmd FileType tex lua on_latex_filetype()")
A.nvim_command("autocmd FileType latex lua on_latex_filetype()")
A.nvim_command("autocmd FileType markdown lua on_latex_filetype()")

-- Setup some bash-keybindings
function on_bash_filetype()
    vim.api.nvim_set_keymap("n", leader .. "ll", [[:w<CR>:split term://bash %<CR>a]], {noremap = true})
end

A.nvim_command("autocmd FileType sh lua on_bash_filetype()")


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

-- Copilot toggling

_G.copilot_enabled = true

function toggle_github_copilot()
    if _G.copilot_enabled then
        vim.cmd("Copilot disable")
        _G.copilot_enabled = false
        vim.notify("Github Copilot disabled")
    else
        vim.cmd("Copilot enable")
        _G.copilot_enabled = true
        vim.notify("Github Copilot enabled")
    end
end

vim.api.nvim_set_keymap("n", "<leader>cc", ":lua toggle_github_copilot()<CR>", {noremap = true, silent = true})



