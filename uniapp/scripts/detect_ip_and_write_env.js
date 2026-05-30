const os = require('os')
const fs = require('fs')
const path = require('path')

function getLocalIPv4() {
  const nets = os.networkInterfaces()
  const candidates = []
  for (const name of Object.keys(nets)) {
    for (const net of nets[name]) {
      if (net.family === 'IPv4' && !net.internal) {
        // skip APIPA
        if (net.address.startsWith('169.254.')) continue
        candidates.push(net.address)
      }
    }
  }
  // prefer private ranges
  const prefer = candidates.find(ip => ip.startsWith('192.') || ip.startsWith('10.') || ip.startsWith('172.'))
  return prefer || candidates[0] || '127.0.0.1'
}

function writeEnv(ip) {
  const repoRoot = path.resolve(__dirname, '..')
  const examplePath = path.join(repoRoot, '.env.development.example')
  const envPath = path.join(repoRoot, '.env.development')
  let content = ''
  if (fs.existsSync(examplePath)) {
    content = fs.readFileSync(examplePath, 'utf8')
  }
  const apiUrl = `http://${ip}:8000`
  const line = `VITE_API_BASE_URL=${apiUrl}`

  if (content.includes('VITE_API_BASE_URL=')) {
    content = content.replace(/VITE_API_BASE_URL=.*/g, line)
  } else {
    if (content && !content.endsWith('\n')) content += '\n'
    content += line + '\n'
  }

  fs.writeFileSync(envPath, content, 'utf8')
  console.log(`[detect_ip_and_write_env] Wrote ${envPath} with ${apiUrl}`)
}

const ip = getLocalIPv4()
writeEnv(ip)
