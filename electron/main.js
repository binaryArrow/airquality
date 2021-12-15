const {app, BrowserWindow} = require('electron')
const path = require("path");
//const backend = require("../backend/dist/main")
const fork = require("child_process").fork
const child = fork('../backend/dist/main')

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
    // startBackend()
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

// function startBackend() {
//     spawn(
//         "npm run start",
//         {
//             cwd: path.join(__dirname, "../backend")
//         }
//     )
// }


