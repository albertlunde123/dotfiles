require'quarto'.setup{
  lspFeatures = {
    enabled = true,
    languages = { 'r', 'python', 'julia' },
    diagnostics = {
      enabled = true,
    },
  }
}
