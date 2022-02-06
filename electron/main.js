const {app, BrowserWindow} = require('electron')
const path = require("path");

function createWindow() {
    win = new BrowserWindow({
        show: false,
        width: 1200,
        height: 900,
        webPreferences: {
            nodeIntegration: true
        }
    })
    win.loadFile('dist/index.html')
}

app.whenReady().then(() => {
    createWindow()
    win.maximize()
    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0)
            createWindow()
    })
})

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin')
        app.quit()
})



