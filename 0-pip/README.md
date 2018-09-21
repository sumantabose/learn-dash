# Install and use pip on macOS without sudo/admin access

Most recently tested on OS X El Capitan (10.11.6) by Sumanta Bose.

1. Install the script `python ./get-pip.py --user`. It is downladed from `https://bootstrap.pypa.io/get-pip.py`
2. Run the installation, appending the `--user` flag. pip will be installed to ~/Library/Python/2.7/bin/pip
3. Make sure `~/Library/Python/2.7/bin` is in your `$PATH`. For `bash` users, edit the `PATH=` line in `~/.bash_profile` to append the local Python path; ie. `PATH=$PATH:~/Library/Python/2.7/bin`. Apply the changes, `source ~/.bash_profile`.
4. Use pip! Remember to append `--user` when installing modules; ie. `pip install <package_name> --user`. However I found this to be optional.

## Note

This has been taken from [here](https://gist.github.com/haircut/14705555d58432a5f01f9188006a04ed). Visit for more info.