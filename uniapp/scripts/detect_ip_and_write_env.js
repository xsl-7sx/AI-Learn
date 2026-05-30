const os = require('os')
const fs = require('fs')
const path = require('path')

function getLocalIPv4() {
  const nets = os.networkInterfaces()
  const candidates = []
  for (const name of Object.keys(nets)) {
    for (const net of nets[name]) {
      if (net.family === 'IPv4' && !net.internal) {
        if (net.address.startsWith('169.254.')) continue
        candidates.push(net.address)
      }
    }
  }
  const prefer = candidates.find(
    (ip) => ip.startsWith('192.') || ip.startsWith('10.') || ip.startsWith('172.'),
  )
  return prefer || candidates[0] || '127.0.0.1'
}

function upsertApiUrl(content, apiUrl) {
  const line = `VITE_API_BASE_URL=${apiUrl}`
  if (content.includes('VITE_API_BASE_URL=')) {
    return content.replace(/VITE_API_BASE_URL=.*/g, line)
  }
  if (content && !content.endsWith('\n')) content += '\n'
  return `${content}${line}\n`
}

function writeEnvFile(envPath, examplePath, apiUrl) {
  let content = ''
  if (fs.existsSync(examplePath)) {
    content = fs.readFileSync(examplePath, 'utf8')
  } else if (fs.existsSync(envPath)) {
    content = fs.readFileSync(envPath, 'utf8')
  }
  fs.writeFileSync(envPath, upsertApiUrl(content, apiUrl), 'utf8')
  console.log(`[detect_ip_and_write_env] Wrote ${envPath} with ${apiUrl}`)
}

function writeEnv(ip) {
  const repoRoot = path.resolve(__dirname, '..')
  const examplePath = path.join(repoRoot, '.env.development.example')
  const apiUrl = `http://${ip}:8000`

  writeEnvFile(path.join(repoRoot, '.env.development'), examplePath, apiUrl)
  // build:mp-weixin 走 production 模式，只读 .env.production
  writeEnvFile(path.join(repoRoot, '.env.production'), examplePath, apiUrl)
}

const ip = getLocalIPv4()
writeEnv(ip)
