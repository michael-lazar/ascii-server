# ascii-server

This is the source for the in-flux django server powering [https://ascii.mozz.us](https://ascii.mozz.us).

Note: this is different from [the ASCII Art Emporium](https://ascii.mozz.us:7070), which is a gopher server running on port 7070.

It's also different from my personal gallery, which is a static file server at [https://mozz.us/ascii-art.html](https://mozz.us/ascii-art.html).

It's also different from [https://aa.mozz.us](https://a.mozz.us), which is my Japanese Shift-JS art collection.

## Requirements

- python3.11

## Quickstart

```bash
# Download the source
git clone https://github.com/michael-lazar/ascii-server
cd ascii-server/

# Initialize a virtual environment and install pip dependencies, etc.
tools/boostrap

# Create a user account for the admin dashboard
tools/manage createsuperuser

# Launch a local server
tools/start

# Initialize pre-commit hooks
pre-commit install

# Run the tests, linters, etc.
tools/pytest
tools/mypy
tools/lint

# Rebuild requirements
tools/pip-compile
tools/pip-install

# Find your house
telnet mapscii.me
```

## License

[The Human Software License](https://license.mozz.us)

> A hobbyist software license that promotes maintainer happiness
> through personal interactions. Non-human
> [legal entities](https://en.wikipedia.org/wiki/Legal_person) such as
> corporations and agencies aren't allowed to participate.

## Miscellaneous

```
          
                                                                `7     
                                                                /     
                                         ,- __                 ,     
     ,                                         ``--  __       /     
     \               .--.          .--.         .--.   ``--.-/.__     
      \             &____]        &____]       (&_.=`7    (_/&=`/     
       \           "-== --'      L.-----"     <'_,- (    -/_)- ( \     
        \           %\_ "%        %" _/%".     %%%"_/  _/` /%"_/ ]     
         \         /`  `- \     -" '\ |   \   /   / `"'-  /  ' ` /     
          \       ! _-'   /!   [   . 't \ |  |     _ .--"`   /  /     
          ,\-_.-.-"    _,  |    \   \  ./ .  !_   / /`   ! _'  '!     
          "--(_,_ __--`-.\ /     ".  .__! |   \____ |    [____ /     
                 `  7"==--<      / \  `=] !   / /`"=|    /  /``]     
                   / | /__ \    /,-`"\ '\_l  / /   `]   /  !   |     
                  /  L --  /   ['     `.-`r)'  |    /  //  ,   /     
                  /,       |   | _.-  \ \_^.  |   ! \  /  /    |     
                 /  .   /  '   |         !/ '.    |  \'  '    ,|     
                //  |  /  /    \    / \ .\ ,  `. /|  !   !   / |     
               //   |  !  |    |_.-"   \| \_.   '.|  |  /|   |||     
              // /  '  ,  |   [_        /  \    / `. | ' /  / !!     
              "~.__/_./___]   / `,___,___--"`-_____-'. _..__.__]     
                 |  /  \  |  |  /    |  | /     \  ! /`.   \  |     
                 ! [    l !  / /      \ !|       . |/   `/  ] !     
                 | /    \ ( / /       | ||       | |        \ |     
                !_(      )_'_(        !_ !       |_'        )_|     
     mozz       (_/      \_! _,       ',_)       '._)       [__,     
```
