# history-view
A little tool to visually browse your console history.

What it looks like to scan through your history now:
    
![calling_it_workin](https://user-images.githubusercontent.com/479566/123533473-de861880-d6ca-11eb-8da0-d7b0d7734814.gif)

### Arguments

`-s, --search`: Search by regex

Supports filtered browsing by passing -s parameter. 

## Known Issues

- Still uses `subprocess` to invoke. It should be _mostly_ the same given that environment variables are passed in, but a straightforward return of the command is something that would be better.
- Only supports Windows and Powershell.
- Only adds to the long-term history. Not the history of the current shell (available via up/down)

### Addendum

Yes, I am entirely aware that I could get the same affect in powershell with `Get-History`. Not the point!