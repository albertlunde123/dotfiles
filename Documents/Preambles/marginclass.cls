\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{margindoc}[2023/10/12 v1.0 Custom class with margin features]

\LoadClassWithOptions{book}% Derived from the book class

% Required packages
\RequirePackage{geometry}
\RequirePackage{sidenotes}
\RequirePackage{caption}
\RequirePackage{background}
\RequirePackage{tikz}
\RequirePackage{graphicx}

% Geometry for wide right margin


\DeclareOption{10pt}{\renewcommand{\normalsize}{\fontsize{10}{12}\selectfont}}
\DeclareOption{11pt}{\renewcommand{\normalsize}{\fontsize{11}{13.6}\selectfont}}
\DeclareOption{12pt}{\renewcommand{\normalsize}{\fontsize{12}{14.5}\selectfont}}

\ExecuteOptions{12pt} % Default option
\ProcessOptions\relax

\geometry{
  paperwidth=215mm,
  paperheight=297mm,
  left=60pt,
  textwidth=320pt,
  marginparsep=10pt,
  marginparwidth=200pt,
  textheight=660pt,
  footskip=40pt
}

\renewcommand{\baselinestretch}{1.3}
% Background line separating main text from margin
\backgroundsetup{
  scale=1,
  color=white,
  opacity=1,
  angle=0,
  position=current page.south,
  vshift=0cm,
  contents={%
    \tikz[remember picture,overlay]
      \draw[line width=0pt] ([xshift=425pt, yshift=100]current page.south west)--([xshift=425pt, yshift=-100pt]current page.north west);
  }
}

\RequirePackage{marginfix}
\RequirePackage{marginnote}
\RequirePackage{caption}

% % Command for figures in the margin
% \newcommand{\marginfig}[3][0pt]{%
%   \marginpar{%
%       \raisebox{#1}{\includegraphics[width=1.0\marginparwidth]{#2}%
%       }
%   \marginnote{%
%       \parbox{\marginparwidth}{\smaller \textbf{figure:} #3}
%   }
% }

% \usepackage{marginnote}
% \usepackage{graphicx}

% \newcommand{\marginfig}[4][0pt]{%
%   \marginpar{%
%     \raisebox{#1}{%
%       \includegraphics[width=\marginparwidth]{#2}%
%       \captionof{figure}{#4}%
%       \label{fig:#3}%
%     }%
%   }%
% }
% % \newcommand{\marginfig}[2][0pt]{%
% %   \marginpar{\raisebox{#1}{%
% %       \includegraphics[width=1.0\marginparwidth]{#2}
% %       % \label{fig:#3}
% %       % \caption{#4}
% %       % \parbox{\marginparwidth}{\smaller \textbf{figure:} #3}%
% %   }}%
% % }
% \newcommand{\margintext}[2][0pt]{%
%   \marginpar{\raisebox{#1}{%qq
%     \parbox{\marginparwidth}{\smaller \textbf{figure:} #2}%
%     }}%
% }

% \newcommand{\marginmath}[2][0pt]{%
%   \marginpar{\raisebox{#1}{%
%     \parbox{1.2\marginparwidth}{#2}%
%     }}%
% }

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
% \titleformat{\section}[frame]{\normalfont\bfseries
% }{\filright
% \footnotesize
% \enspace Section \thesection \enspace
% }{4pt}{\normalfont\large\filcenter}% section format
\titleformat{\section}[hang]{\normalfont\bfseries
}{\filright
% \footnotesize
\enspace \thesection
}{4pt}{\normalfont\bfseries\itshape}% subsection format

% subsection format that allows linebreaks in the title if it is too long to fit
% subsection with line after title

\titleformat{\subsection}[hang]{\normalfont\bfseries
}{\filright
\footnotesize
\enspace \thesubsection \enspace
}{4pt}{\normalfont\bfseries\itshape}% subsection format


\RequirePackage{fancyhdr}% load the helper package
\fancypagestyle{normal}{
    % \renewcommand{\headrulewidth}{0.4pt}% The running heads and feet do not have rules
    % \renewcommand{\footrulewidth}{0pt}
    \fancyhf{}% set up the page numbering 
    \fancyfoot[C]{\efbox[margin = 10pt,
                      topline = true,
                      leftline = false,
                      rightline = false,
                      bottomline = false,
                      backgroundcolor = background,
                      linewidth = 1pt,
                      linecolor = foreground]{\thepage\ of \pageref{LastPage}}}
    \fancyhead[R]{}
    \fancyhead[L]{}
    \renewcommand{\footrulewidth}{0pt}
    \renewcommand{\headrulewidth}{0pt}
}

% This is used for chapters
% Redefine the plain page style
\fancypagestyle{plain}{%
  \fancyhf{}%
  \fancyfoot[C]{\efbox[margin = 10pt,
                      topline = true,
                      leftline = false,
                      rightline = false,
                      bottomline = false,
                      backgroundcolor = background,
                      linewidth = 1pt,
                      linecolor = foreground]{\thepage\ of \pageref{LastPage}}}
  \fancyhead[R]{Albert Lunde}
  \fancyhead[L]{}
  \renewcommand{\headrulewidth}{0pt}% Line at the header invisible
  \renewcommand{\footrulewidth}{0pt}% Line at the footer visible
}

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

\endinput
