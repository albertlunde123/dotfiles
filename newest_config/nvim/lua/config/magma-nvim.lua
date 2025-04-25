-- local magma = require('magma')
-- magma.setup()

local function map(m, k, v)
	vim.keymap.set(m, k, v, {silent = true})
end

vim.g.magma_image_provider = 'kitty'

map('n', '<leader>r', '<cmd>MagmaEvaluateOperator<cr>')
map('n', '<leader>rr', '<cmd>MagmaEvaluateLine<cr>')
map('x', '<leader>r', '<cmd>MagmaEvaluateVisual<cr>')
map('n', '<leader>ro', '<cmd>MagmaShowOutput<cr>')

function MagmaInitPython()
    vim.cmd[[
    :MagmaInit python
    :MagmaEvaluateArgument a=5
    ]]
end

vim.cmd[[
:command MagmaInitPython lua MagmaInitPython()
]]
