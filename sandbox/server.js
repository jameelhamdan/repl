import {Server} from "socket.io";
import Repl from "./src/repl.js";
import IConsoles from "./src/iconsole.js";

// Config
const port = 8000;

const io = new Server(port, {
    path: '',
    cors: {
        origin: '*',
    }
});

// Global instance of Repl
let _Repl = new Repl(IConsoles.Cmd, (data) => {
    io.emit('stdout', data);
});

io.on("connection", (socket) => {
    console.log('Client Connected');

    // TODO: Send this in chunks instead of one message at a time
    _Repl.messages.forEach(m => socket.emit('stdout', m));

    socket.on('input', (msg) => {
        _Repl.write(msg);
    });
    socket.on('disconnect', () => {
        console.log('Client disconnected');
    });
});

console.log(`Starting Server on port ${port}`)
console.log(`Press Ctrl + C to stop server.`)
