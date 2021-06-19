# history-view
A little tool to visually browse your console history.

What it looks like to scan through your history now:
    
![more_scrolling](https://user-images.githubusercontent.com/479566/122635631-f2fa5d80-d099-11eb-9e72-cb83441c1c54.gif)

TODO:
- [ ] How do we display the same "screen" when rendering?
- [ ] How do we listen to up/down arrow?
- [ ] How do we pass the I/O around?
- [ ] Correct console loop, no hacks.
    - Gonna need to buffer each line with whitespace so that it overwrites properly :/ 

## How can we listen to up/down arrow AND do inputy things?

After looking into a couple different libraries, I think `pynput` is probably the way to go. From their readme:

```python
from pynput import keyboard

def on_press(key):
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k in ['1', '2', 'left', 'right']:  # keys of interest
        # self.keys.append(k)  # store it in global-like variable
        print('Key pressed: ' + k)
        return False  # stop listener; remove this if want more keys

listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread
listener.join()  # remove if main thread is polling self.keys
```

## How do we actually consume the output of `history-view`?

We need a good way to take the command output as the result of this little package. Python's buildin module `atexit` is pretty nice, but I don't see how I can set the next terminal values.

I believe the answer here lies in a `shim` that calls `history-view`. Here's why I think that.

1. User is like "I need to dig into my history and find that command I used before"
2. `hv`
3. User finds their command, selects it, presses `enter`. 
4. ???

How do we ensure that the experience is _the same_ as if we had entered that text directly from the command line?

`subprocess.Popen("<command> <commandarg1> <commandarg2> ...", shell=True)` would _probably_ work, but how can we be _certain_ that we're entirely the same?

Remove ourselves from the equation, that's how. The only way that I can think of to DO this right now is to simply add _another_ shim on top of the one defined in `console_scripts`.

This way, when a user invokes `hv`, instead of simply calling the python and exiting, it should PIPE the selected command to an invocation on the terminal. Equivalent in powershell would be

`hv | $_`

"Take the output, invoke it".

Short term, I believe I'm going to go the `popen` route to make forward progress. I will note that another issue with the `popen` route is that the command that you DID select won't be in your history for an easy up-arrow retrieval either. That's also a gamebreaker.
