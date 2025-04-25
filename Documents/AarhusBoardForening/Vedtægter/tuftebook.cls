\NeedsTeXFormat{LaTeX2e}
\ProvidesFile{tuftebook.cls}[2020/03/24 v1.00a Caesar book]
% Load the amsmath and the mhchem package before loading microtype
\RequirePackage[version=4]{mhchem}
\RequirePackage{amsmath}% better math handling
\LoadClassWithOptions{book}% this is derived from the book class
\RequirePackage{sidenotes}% put annotations, tables and figures in the margin
\captionsetup{font=footnotesize, skip=4pt}
\RequirePackage[maxfloats=45]{morefloats}% a lot of marginals need more float 'memory'
% VERY IMPORTANT: use latest version of marginfix!
% https://github.com/shicks/marginfix/releases/tag/v1.2
% Otherwise, some sidenotes get dropped!!!
\RequirePackage{marginfix}% automatically adjust the side-floats nicely 
\newcommand{\caesar@letterspace}[1]{#1}% allow LuaLaTeX, LaTeX letterspacing
% \RequirePackage[letterspace=150]{microtype}% microtypography
% \@ifpackagelater{microtype}{2011/08/18}% xxx allow LaTeX and earlier microtype
% {\renewcommand{\caesar@letterspace}[1]{\textls{#1}}}%
% {\AtEndDocument{\ClassWarningNoLine{caesar_book}{Need newest microtype for letterspacing.}}}
%
% Set page layout geometry -- default is science-book format
% this means a (portrait) paper size of 170mm x 240mm
%
\RequirePackage{geometry}
\geometry{
paperwidth=215mm,
paperheight=297mm,
% left=80pt,
top=70pt,
textwidth=400pt,
marginparsep=20pt,
marginparwidth=180pt,
textheight=660pt,
footskip=40pt
}
% \RequirePackage{fouriernc}
%
% fontsize is 10pt with a leading (line spacing) of 13pt for book 
%
\renewcommand{\normalsize}{\fontsize{10pt}{13pt}\selectfont}%
\renewcommand{\footnotesize}{\fontsize{8pt}{10pt}\selectfont}%
% fullwidth environment, text across textwidth+marginparsep+marginparwidth
\newlength{\overhang}
\setlength{\overhang}{\marginparwidth}
\addtolength{\overhang}{\marginparsep}
%
\newenvironment{fullwidth}
  {\ifthenelse{\boolean{@twoside}}%
     {\begin{adjustwidth*}{}{-\overhang}}%
     {\begin{adjustwidth}{}{-\overhang}}%
  }%
  {\ifthenelse{\boolean{@twoside}}%
    {\end{adjustwidth*}}%
    {\end{adjustwidth}}%
  }


\RequirePackage{titlesec,titletoc}% load the helper package
\RequirePackage{fmtcount}
\RequirePackage{efbox}




\titleformat{\chapter}[display]
{\bfseries\Large}
{}
{0pt}
{\titlerule
\vspace{1.5ex}%
\filcenter}
[\vspace{1.5ex}%
\titlerule]
\titlespacing*{\chapter}{0pt}{-40pt}{10pt}
% \setcounter{secnumdepth}{-1}% no numbering at all
% syntax for titleformat
% \titleformat{<format>}[<placement>]{<formatting>}{<label>}{<space before>}{<space after>}
\titleformat{\section}[hang]{\normalfont\bfseries
}{
\normalfont\bfseries
\enspace § \thesection \enspace
}{4pt}{\normalfont\bfseries\large}% section format

% subsection format that allows linebreaks in the title if it is too long to fit
% subsection with line after title

\titleformat{\subsection}[hang]{\normalfont\bfseries
}{\filright
\footnotesize
\enspace \thesubsection \enspace
}{4pt}{\normalfont\bfseries\itshape}% subsection format


% \RequirePackage{fancyhdr}% helper package
% \renewcommand{\headrulewidth}{0pt}% The running heads and feet do not have rules
% \renewcommand{\footrulewidth}{0pt}
% \fancyhf{}% set up the page numbering 
% {\fancyfoot[LE,RO]{\thepage}}
% \fancypagestyle{plain}{%
% 	\fancyhf{}
% }

\RequirePackage{emptypage}

% \makeatletter
% \def\cleardoublepage{\clearpage\if@twoside \ifodd\c@page\else
% \hbox{}
% \vspace*{\fill}
% \begin{center}
% This page intentionally contains only this sentence.
% \end{center}
% \vspace{\fill}
% \thispagestyle{empty}
% \newpage
% \if@twocolumn\hbox{}\newpage\fi\fi\fi}
% \makeatother





% Also show page numbers on first page of chapter
\usepackage{etoolbox} 
\patchcmd{\chapter}{\thispagestyle{plain}}{\thispagestyle{fancy}}{}{}




\renewcommand{\frontmatter}{\pagestyle{empty}}% the frontmatter is empty
\renewcommand{\mainmatter}{\cleardoublepage\pagestyle{fancy}}% mainmatter with page numbering
\RequirePackage{ragged2e} % \RaggedRight works better than \raggedright
\newcommand{\marginparstyle}{\footnotesize} % initialize style with start value
\long\def\@ympar#1{% redefine margin par to avoid too many macros in the document
  \@savemarbox\@marbox{\marginparstyle#1}% marginparstyle is a prefix to the marginpar text now
  \global\setbox\@currbox\copy\@marbox % the rest of the definition is taken from original LaTeX
  \@xympar}
\renewcommand*{\marginfont}{\marginparstyle}
% setup itemize and enumerate  
\RequirePackage[shortlabels]{enumitem}
\setlist[itemize]{leftmargin=*}
%\renewcommand{\labelitemi}{}
% compatibility with T-L


\newcommand\newthought[1]{%
   \addvspace{1.0\baselineskip plus 0.5ex minus 0.2ex}%
   \noindent\textsc{#1}%
}%
\ExplSyntaxOn
\NewDocumentCommand \sidecite { o o m }
{ 
  \IfNoValueOrEmptyTF{#1}
  {
    \IfNoValueOrEmptyTF{#2}
    {
      \sidenote{\fullcite{#3}}
    }
    {
      \sidenote{\fullcite[#2]{#3}}
    }
  }
  {
    \IfNoValueOrEmptyTF{#2}
    {
      \sidenote{\fullcite[#1]{#3}}
    }
    {
      \sidenote{\fullcite[#1][#2]{#3}}
    }
  }
}
\ExplSyntaxOff

\RequirePackage{caption}
% \RequirePackage[margincaption,outercaption,,wide]{sidecap}
% \sidecaptionvpos{figure}{t} 
\captionsetup{labelfont={sf,bf,footnotesize}}
\DeclareCaptionStyle{marginfigure}[]{labelfont={sf,bf,footnotesize}, font=footnotesize, justification=justified}
\DeclareCaptionStyle{sidecaption}[]{labelfont={sf,bf,footnotesize}, font=footnotesize, justification=justified, singlelinecheck=off}
\DeclareCaptionStyle{widefigure}[]{labelfont={sf,bf,footnotesize}, font=footnotesize}

\renewcommand{\normalsize}{\fontsize{10pt}{13pt}\selectfont}%
\renewcommand{\footnotesize}{\fontsize{8pt}{10pt}\selectfont}%
