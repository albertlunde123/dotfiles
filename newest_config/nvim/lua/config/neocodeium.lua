local neocodeium = require("neocodeium")
neocodeium.setup()
vim.keymap.set("i", "b", neocodeium.accept)
vim.keymap.set("i", "<c-b>", neocodeium.cycle)

