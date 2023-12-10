require("telescope").setup {
   -- ignore latex auxilliary files
    defaults = {
        file_ignore_patterns = { ".*%.aux", ".*%.toc", ".*%.out", ".*%.log", ".*%.synctex.gz", ".*%.fdb_latexmk", ".*%.fls", ".*%.bcf", ".*%.bbl", ".*%.blg", ".*%.run.xml", ".*%.svg", ".*%.pdf_tex"},
    }
}
