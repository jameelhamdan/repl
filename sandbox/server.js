import {Server} from "socket.io";
import Repl from "./src/repl.js";
import Terminals from "./src/terminal.js";

const port = 8000;

const io = new Server(port, {
    path: '',
    cors: {
        origin: '*',
    }
});

// Get Argument for which Terminal to run
const arg = process.argv[2] || 'cmd';
const terminal = Terminals[arg];

if (!terminal) {
    console.error(`Terminal with name "${arg}" undefined`);
    process.exit(1);
}

// Global instance of Repl
let repl = new Repl(terminal, (data) => {
    io.emit('stdout', data);
});

io.on("connection", (socket) => {
    console.log('Client Connected');

    // TODO: Send this in chunks instead of one message at a time
    repl.messages.forEach(m => socket.emit('stdout', m));

    socket.on('input', (msg) => repl.write(msg));

    socket.on('disconnect', () => {
        console.log('Client disconnected');
    });
});

console.log(`Starting Server on port ${port}`)
console.log(`Press Ctrl + C to stop server.`)
