-- local vimtex = require('vimtex')

-- vimtex.setup({
--   tex_flavor = 'mklatex',
--   vimtex_view_general_viewer = 'zathura'
-- }
--
vim.g.tex_flavor = 'latexmk'
vim.g.vimtex_view_general_viewer = 'zathura' 
vim.g.vimtex_syntax_enabled = 1
vim.g.vimtex_quickfix_mode = 1
vim.g.vimtex_quickfix_open_on_warning = 0
vim.g.vimtex_compiler_latexmk = {
  options = {
    '--shell-escape',
    '--synctex=1',
    '-interaction=nonstopmode',
    '-file-line-error',
  }
}
vim.g.vimtex_compiler_latexmk_engies = {
  ['_'] = '-lualatex',
  ['latex'] = '-pdf',
  ['pdflatex'] = '-pdf',
  ['xelatex'] = '-xelatex',
}
-- vim.g.vimtex_syntax_custom_cmds|
-- vim.g.vimtex_syntax_conceal = '1'
-- vim.g.vimtex_syntax_conceal_cites|
-- vim.g.vimtex_syntax_conceal_disable|
-- vim.g.vimtex_syntax_nested|
-- vim.g.vimtex_syntax_packages|
-- vim.g.vimtex_quickfix_mode= 0
-- vim.g.Tex_MultipleCompileFormats = 'pdf,bib,pdf'
