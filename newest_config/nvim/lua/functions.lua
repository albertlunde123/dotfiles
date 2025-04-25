function WriteSel(filename)
    -- Get the start and end of the visual selection
    local start_line, start_col, end_line, end_col = unpack(vim.fn.getpos("'<"))
    local _, _, _, end_col_line_end = unpack(vim.fn.getpos("'>"))

    -- Adjust the column indices for Lua (0-indexed)
    start_col = start_col - 1
    end_col = end_col - (end_col_line_end == 0 and 1 or 0)

    -- Get the lines in the visual selection
    local lines = vim.api.nvim_buf_get_lines(0, start_line-1, end_line, false)

    -- Adjust the first and last line to match the visual selection
    lines[1] = lines[1]:sub(start_col+1)
    lines[#lines] = lines[#lines]:sub(1, end_col)

    -- Write the lines to the file
    local file = io.open(filename, "w")
    for _, line in ipairs(lines) do
        file:write(line, "\n")
    end
    file:close()
end

-- function that comments out everything but the body of the latex file.
--

function toggle_comment_latex()
    local start_pattern = "begin{document}"
    local end_pattern = "end{document}"

    -- Find start and end of the document body
    local start_pos = vim.fn.searchpos(start_pattern, 'nW')[1]
    local end_pos = vim.fn.searchpos(end_pattern, 'nW')[1]

    if start_pos == 0 or end_pos == 0 then
        print("Document body not found")
        return
    end

    local function toggle_comment_line(line)
        if line:sub(1, 1) == '%' then
            return line:sub(2)  -- Uncomment
        else
            return '%' .. line  -- Comment
        end
    end

    -- Toggle comment for everything before start
    for i = 1, start_pos do
        local line = vim.fn.getline(i)
        vim.fn.setline(i, toggle_comment_line(line))
    end

    -- Toggle comment for everything after end
    for i = end_pos, vim.fn.line('$') do
        local line = vim.fn.getline(i)
        vim.fn.setline(i, toggle_comment_line(line))
    end
end

-- Optional: bind the function to a keybinding in Neovim
-- vim.api.nvim_set_keymap('n', 'bb', ':lua toggle_comment_latex()<CR>', { noremap = true, silent = true })
