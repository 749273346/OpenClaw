module.exports = {
  apps: [{
    name: "hdb-agent",
    script: "openclaw",
    args: "gateway run --force",
    cwd: "/root/.openclaw",
    interpreter: "node",
    exec_mode: "fork",
    autorestart: true,
    watch: false,
    max_memory_restart: "1G",
    env: {
      NODE_ENV: "production",
      // Ensure PATH includes the location of openclaw binary if needed, 
      // but usually PM2 inherits environment.
    },
    error_file: "/root/.openclaw/logs/pm2-error.log",
    out_file: "/root/.openclaw/logs/pm2-out.log",
    merge_logs: true,
    time: true
  }]
};
