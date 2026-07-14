# PalTool 图片补全任务（给 小马/Marvis）

## 任务目标
为 PalTool 网站（paltool.cc）补全 141 张缺失的帕鲁图片。

## 数据位置
本地路径：D:\幻兽帕鲁\paltool\
现有图片：D:\幻兽帕鲁\paltool\img\pals\（159张已有）
缺失图片：141张（清单见下方）

## 图片规格要求
- 格式：PNG（带透明背景）
- 尺寸：推荐 128×128 或 64×64 像素（矩形带圆角）
- 命名规则：`{pal_id}.png`（例：`flyingmanta_thunder.png`）

## 数据来源（按优先级）

### 方案A：palworld.wiki.gg 维基（推荐）
- 网址：https://palworld.wiki.gg/wiki/{PalName}
- 图片URL：https://palworld.wiki.gg/wiki/Special:FilePath/{PalName}.png
- 说明：维基上有大部分帕鲁的图片，但文件名可能与显示名不一致
- 示例：搜索 "Celaray Lux" → 查看页面源码找 `<img>` 标签的 src

### 方案B：paldb.cc（数据最全）
- 网址：https://paldb.cc/en/{PalName}
- 说明：所有帕鲁的完整数据+图片，但做了反扒（curl会403）
- 需要通过浏览器打开页面，查看元素从HTML里提取图片URL

### 方案C：Palworld 游戏文件提取（一劳永逸）
- 从 Palworld 游戏安装目录提取图标文件
- 位置通常在：`Pal/Content/Pal/UI/` 或类似路径
- 需要解包 .pak 文件
- 这是最准确的方式，文件名直接对应

## 缺图清单（141只）

每条格式：`图鉴编号 显示名 (id=内部ID)`

```
#    7 Celaray Lux               (id=flyingmanta_thunder)
#    9 Croajiro Noct             (id=kendofrog_dark)
#   10 Herbil                    (id=leafmomonga)
#   13 Pupperai                  (id=samuraidog)
#   14 Clovee                    (id=cloverfairy)
#   17 Pengullet Lux             (id=penguin_electric)
#   18 Penking Lux               (id=captainpenguin_black)
#   23 Tanzee Ignis              (id=monkey_fire)
#   29 Foxparks Cryst            (id=kitsunebi_ice)
#   30 Killamari Primo           (id=negativeoctopus_neutral)
#   34 Caprity Noct              (id=berrygoat_dark)
#   37 Turtacle                  (id=tentacleturtle)
#   37 Turtacle Terra            (id=tentacleturtle_ground)
#   39 Woolipop Terra            (id=sweetssheep_ground)
#   41 Azurobe Cryst             (id=bluedragon_ice)
#   44 Ribbuny Botan             (id=pinkrabbit_grass)
#   45 Jelliette                 (id=jellyfishfairy)
#   46 Jellroy                   (id=jellyfishghost)
#   47 Amione                    (id=clionetwins)
#   48 Gloopie                   (id=octopusgirl)
#   48 Gloopie Primo             (id=octopusgirl_neutral)
#   50 Wispaw                    (id=ghostblackcat)
#   54 Univolt Cryst             (id=kirin_ice)
#   56 Loupmoon Cryst            (id=werewolf_ice)
#   59 Muffly                    (id=fluffybird)
#   62 Puffolt                   (id=elecpomeranian)
#   72 Polapup                   (id=iceseal)
#   72 Polapup Terra             (id=iceseal_ground)
#   78 Wixen Noct                (id=foxmage_dark)
#   79 Katress Ignis             (id=catmage_fire)
#   81 Elgrove                   (id=grassminotaur)
#   81 Elgrove Cryst             (id=grassminotaur_ice)
#   83 Fenglope Lux              (id=fengyundeeper_electric)
#   85 Bushi Noct                (id=ronin_dark)
#   86 Munchill                  (id=icecrocodile)
#   88 Finsider                  (id=stuffedshark)
#   88 Finsider Ignis            (id=stuffedshark_fire)
#   89 Petallia Ignis            (id=flowerdoll_fire)
#   90 Leafan                    (id=pandagirl)
#   92 Dazzi Noct                (id=raijindaughter_water)
#   96 Beakon Cryst              (id=thunderbird_ice)
#   97 Ghangler                  (id=ghostanglerfish)
#   97 Ghangler Ignis            (id=ghostanglerfish_fire)
#   98 Rayhound Cryst            (id=thunderdog_ice)
#   99 Menasting Terra           (id=darkscorpion_ground)
#  100 Needoll                   (id=cactusdoll)
#  100 Needoll Noct              (id=cactusdoll_dark)
#  105 Moldron                   (id=volcanodragon)
#  105 Moldron Cryst             (id=volcanodragon_ice)
#  106 Palumba                   (id=tropicalostrich)
#  109 Dumud Gild                (id=lazycatfish_gold)
#  110 Braloha                   (id=plesiosaur)
#  111 Kitsun Noct               (id=amaterasuwolf_dark)
#  113 Warsect Terra             (id=herculesbeetle_ground)
#  114 Frostplume                (id=snowpeafowl)
#  115 Majex                     (id=darkflamefox)
#  116 Sibelyx Primo             (id=whitemoth_neutral)
#  119 Icelyn                    (id=icewitch)
#  120 Gildra                    (id=mummypal)
#  124 Quivern Botan             (id=skydragon_grass)
#  128 Skutlass                  (id=swordcutlassfish)
#  128 Skutlass Ignis            (id=swordcutlassfish_fire)
#  130 Starryon                  (id=nightbluehorse)
#  130 Starryon Primo            (id=nightbluehorse_neutral)
#  131 Pierdon                   (id=rockbeast)
#  131 Pierdon Cryst             (id=rockbeast_ice)
#  132 Cryolinx Terra            (id=whitetiger_ground)
#  133 Snugloo                   (id=smallyeti)
#  136 Carnibora                 (id=venusflytrap)
#  137 Blazamut Ryu              (id=kingbahamut_dragon)
#  138 Dualith                   (id=grassgolem)
#  138 Dualith Noct              (id=grassgolem_dark)
#  140 Sekhmet                   (id=sekhmet)
#  141 Prixter                   (id=scorpionman)
#  141 Prixter Lux               (id=scorpionman_electric)
#  142 Tetroise                  (id=cubeturtle)
#  142 Tetroise Primo            (id=cubeturtle_neutral)
#  143 Nyafia                    (id=badcatgirl)
#  148 Nitemary                  (id=ghostrabbit)
#  148 Nitemary Botan            (id=ghostrabbit_grass)
#  149 Smokie                    (id=blackpuppy)
#  149 Smokie Cryst              (id=blackpuppy_ice)
#  150 Omascul                   (id=mysterymask)
#  151 Whalaska                  (id=icenarwhal)
#  151 Whalaska Ignis            (id=icenarwhal_fire)
#  153 Splatterina               (id=grimgirl)
#  154 Gildane                   (id=goldenhorse)
#  156 Bulldosu                  (id=sumodog)
#  157 Celesdir                  (id=whitedeer)
#  157 Celesdir Noct             (id=whitedeer_dark)
#  159 Knocklem Ignis            (id=winggolem_fire)
#  160 Silvegis                  (id=whiteshielddragon)
#  161 Azurmane                  (id=bluethunderhorse)
#  162 Valentail                 (id=longcat)
#  163 Snock                     (id=elecsnail)
#  163 Snock Lux                 (id=elecsnail_ground)
#  164 Souffline                 (id=dandeliongirl)
#  165 Lapiron                   (id=brownrabbit)
#  166 Hoodle                    (id=hoodghost)
#  167 Slowatt                   (id=eleclizard)
#  168 Bakemi                    (id=onighostgirl)
#  169 Solmora                   (id=kingsunfish)
#  169 Solmora Lux               (id=kingsunfish_thunder)
#  170 Lapure                    (id=sleeverabbit)
#  171 Eidrolon                  (id=ghostdragon)
#  171 Eidrolon Ignis            (id=ghostdragon_fire)
#  172 Dynamoff                  (id=thunderfluffybird)
#  173 Tropicaw                  (id=redflowerbird)
#  174 Flaracle                  (id=foxexorcist)
#  175 Ophydia                   (id=lotusdragon)
#  176 Dupin                     (id=clownrabbit)
#  177 Roujay                    (id=thiefbird)
#  178 Venusa                    (id=snakegirl)
#  179 Mycora                    (id=mushroomlady)
#  180 Loomen                    (id=lanternbutler)
#  181 Wistella                  (id=moonchild)
#  182 Solenne                   (id=monochromequeen)
#  183 Renjishi                  (id=kabukiman)
#  184 Aegidron                  (id=domearmordragon)
#  188 Faleris Aqua              (id=horus_water)
#  191 Bastigor                  (id=snowtigerbeastman)
#  192 Shaolong                  (id=blueskydragon)
#  193 Silvance                  (id=mothman)
#  194 Dandilord                 (id=flowerprince)
#  195 Bellanoir                 (id=nightlady)
#  195 Bellanoir Libero          (id=nightlady_dark)
#  196 Xenolord                  (id=darkmechadragon)
#  197 Hartalis                  (id=legenddeer)
#  201 Neptilius                 (id=poseidonorca)
#  203 Panthalus                 (id=kingwhale)
```

## 交付要求
1. 下载的图片放到 `D:\幻兽帕鲁\paltool\img\pals\` 目录
2. 文件名必须是 `{id}.png`（和 pals.json 里的 image 字段一致）
3. 所有图片处理完后，通知赵总验证
4. 如果某张图实在找不到，标注原因（"维基无此帕鲁页面"/"paldb.cc无此帕鲁"等）

## 预期工作量
- 141 张图片
- wiki.gg 方式：约 5-10 分钟（一次性 API 查询）
- paldb.cc 方式：约 1-2 小时（需要逐页查看）
- 游戏文件提取：约 30 分钟（但需要安装游戏）
