function open_floating_window()
    -- Define the size and position of the window
    local width = vim.api.nvim_get_option("columns")
    local height = vim.api.nvim_get_option("lines")
    local win_width = math.ceil(width * 0.4) - 4
    local row = 2
    local col = math.ceil(width * 0.6) + 2

    -- Create a new buffer for the window
    local buf = vim.api.nvim_create_buf(false, true)

    -- Set the buffer's options
    vim.api.nvim_buf_set_option(buf, 'bufhidden', 'wipe')

    -- Read the file's content
    local lines = {}
    for line in io.lines("/home/albert/.config/nvim/GPT4/suggestion.txt") do
        table.insert(lines, line)
    end
    
    local win_height = #lines + 1

    if win_height > math.ceil(height*0.4) then
        win_height = math.ceil(height*0.4)
    end

    local win_config = {
        relative = 'editor',
        width = win_width,
        height = win_height,
        row = row,
        col = col,
        style = 'minimal',
        focusable = true,
        anchor = 'NW',
    }

    -- Create the window
    local win = vim.api.nvim_open_win(buf, true, win_config)

    -- Set the buffer's lines
    vim.api.nvim_buf_set_lines(buf, 0, -1, false, lines)
 -- Create border buffer
    local border_buf = vim.api.nvim_create_buf(false, true)

    -- Create border window
    local border_config = {
        style = "minimal",
        relative = "editor",
        width = win_width + 4,
        height = win_height + 4,
        row = row - 2,
        col = col - 2,
    }

    local border_win = vim.api.nvim_open_win(border_buf, false, border_config)
    vim.cmd(string.format("autocmd WinClosed <buffer=%s> silent lua vim.api.nvim_win_close(%s, true)", buf, border_win))

end

return {
    open_floating_window = open_floating_window,
}

