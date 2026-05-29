import { cpSync, existsSync, mkdirSync, writeFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = join(dirname(fileURLToPath(import.meta.url)), '..')
const source = join(root, 'node_modules', 'towxml')
const target = join(root, 'src', 'wxcomponents', 'towxml')

if (!existsSync(source)) {
  console.warn('[copy-towxml] towxml package not found, skip')
  process.exit(0)
}

mkdirSync(join(root, 'src', 'wxcomponents'), { recursive: true })
cpSync(source, target, { recursive: true })

// towxml 默认用 /towxml/... 绝对路径，uni-app 需改为相对路径
const decodeJson = join(target, 'decode.json')
writeFileSync(
  decodeJson,
  JSON.stringify(
    {
      component: true,
      usingComponents: {
        decode: './decode',
        'audio-player': './audio-player/audio-player',
        latex: './latex/latex',
        table: './table/table',
        todogroup: './todogroup/todogroup',
        yuml: './yuml/yuml',
        img: './img/img',
      },
    },
    null,
    2,
  ) + '\n',
)

console.log('[copy-towxml] copied to src/wxcomponents/towxml')
