Make a StreamTeX course web book called "Software Engineering 1". Create a new project folder for it.

For the content, create blocks appropriate for the following course objectives:

```
```

with the following course description:
```
```

and course assessment:
```
```


Read documentation/streamtex_cheatsheet_en.md to learn how to use streamtex.
Take inspiration from project_aiai18h, its book.py and blocks for how to build a web book with modular blocks that may be nested and reuseable. Use as streamtex functions whenever possible and refrain from using streamlit functions to style the layout. Do NOT write html yourself, use the provided streamtex functions to achieve that. Only use streamlit function for things you cannot achieve with streamtex (having runnable python code blocks, playing audi, etc), and even then, make a block file for these which call the provided streamtex function that wraps streamlit panels and allows them to be integrated with the rest of the blocks and created through a streamtex st_book call.

If you need to run code, first run `conda activate streamtex`.