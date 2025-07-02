


from onekeyinstall.tools.install_top import InstallBtop



btop = InstallBtop()

# print()


for k,v in btop._install.commands.items():
    print(k)
    v()