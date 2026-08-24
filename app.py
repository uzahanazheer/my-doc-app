import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os

st.set_page_config(page_title="ระบบออกใบเสร็จรับเงิน", page_icon="🧾", layout="wide")

# รูปโลโก้ Base64 ถอดแบบจากต้นฉบับ
LOGO_BASE64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAR8AAACACAYAAADU5A1bAAAACXBIWXMAAAsTAAALEwEAmpwYAAAYa0lEQVR4nO2de3ATV37Hv6vXyLIt2/I3+IUPjB3AGAMGTILBSxO3m3S33U23mWRmttvdZjM1M3ez3e3e7f3DduZul/S22/1ju2k3SdpNM3fS3exMkm6Tze0mBvziB8TYGGyjA35AtiVLXqve3x9I1lsjy3qItXp+v3/I4Ovo6Ojo+X3Oued3fud3OBAIBIGgoeYAEIjSAnEkCApA4kgQFIHEkSAoAokjQVAE/1B3AOhM2XoOACy/L1S13x2XvS4A24E9sT86y/sJgiAg/p+e148k4aC2E7sP/69/qXm/1JvG8XG+032l53O2i8aRoIokjgRBEX7xT2o3EACm7/q3f3k7wP031L23pXv/4M8/eL+/q3s/QRAE3pA3f/4/3tLzvX/m7/+sX1N382s2f3e8/426d0s3A/8bdfsnCIKAM/A98aXmfq/e3jI/O+b8T+p/X3eS4P6x5v2u+9m3+qG48yQI/m8X6g7ghm4XkL0T+I++3e++q733yWvvf9+u2e3k712oew/1v/m48eO635/f/s6/1vS8C/A3G/2u/9G051Nf/S3i/14XlA6SxBfS/1f9T5cI1P+z5v4u3Q/88e+83++9i261f+832L9347d4sP/f/72f1x0j/y5O/O4nS/pdaX7242c3/P7f+L14c2f6d4m/uAro19Td6z4k4m0g1f2v52f9j39G3s93f+fD2yvL4u8vV2t/A1z38//jQyT/v+aI1B/S//8+5/38SfvSg6p9n/f+/yJ3j9Xf6L+v3S5A4gj5Rvd9v7TvhzLq37/tWf63k/6S5y5O/O7mneD+Xn10Iq9533c37I1/U9363821035vU/3/e6f9A2Sff6X+O/7+N3+d2N9vff39+rP/S8L3C3Xf1y/eI/Ofe3fN5/f/sC7p+61X+r7/Rk5e6X6H2O/v3l39/L/p3w+1A3oG+16vve/3/f9H/K9/u6m5v8d/f33p5/m+980bfx+/p62NlM41+03e05+81P32s9Ie690f339C/9I+O8lI42878x7p6//07eXv9f2S4/f+/a1/s6X/P16u3v3+d04z0p2y7z420e61I0k8o34D8fIeA/n+A00S6f+tOyr/Xm//vXy//38p/S4f703eA/X3d8L34tqfP/WbfzJ9aX93fX7S95p02n4vXlI+/3a0+9/vJv35S3m/P5S//0XNez//d9zL3i/+Ie33f3+3i+v1b7+7fU/M9f22+P/sF/X93u3y/T/v8y39Xve+f6v+/f/s413G/W/p5539352358/eXf4a//m9Nn1f/2m5fU31fI73/k7339/17//x/uX38X6a/5f/+m2p/2k1P3sP8I3vSvu8s/X51v//iN973X26v/0/234A3v331f2S8fX1I43iSBAU4e3eQ1/31R6JInEkCIpA4kgQFIHEkSAoAokjQVAE4o4E8e3y4f3vA4B2Z476E0FiA1E8CPLbX995A2pX7d287i+RkYdI1/1eH93eZp/fQf/d5+3/k588SvxX5uIqI43kI34q4kQQ5AnFmSB+euvY22m9/e3+gG+72xfg9vt8fAed/p2/fX3vL3//t2894+f03s3m+eT9G0s/q7e/87m89e9/5++fX9n/t6P1O+/++U8f43N5O2X/yR++sX/5fO/4f/j9p9mZp/E6E8S1j7643u70eXy+/e4A6fC3s9vlA9p689v/aMvfJb873+XpIn39vv4ed5v7jR2pX4P/d/S9U43/Xp48EAT1IIn4I63X3e1q43P3kQ3vThqA29uOnR54I3X/l+/s0t7//Gq39j+1t6XpXn9fC3602f3A219U9r/+z0fI/y+S/iA/9u2S3pG/9+3X3e7yS338a0f9f38/98UjSZC4R34a5In2Lq7s2N3B+83b4/C18y49mK856p8A2+2i7v9/X+zX3p+I5J1v+A93x/+33/u3y//u0/2tX9/7v5v5/6XuvxM6v8mHInS3I3HEx38Tf+I/J/9XfL/N8O/e822v09/S1evf6/Bv53/zefk3G8y9T7m3v3sPbf/u6iM27f+248Sft4368++2S+v3f/3N3a3o3e/99443A398a/+/+LpA/I//aE3/S3v/+r/v9/944e/fJv/0X41I/8Pq/31S9319/+/U1n23eH8f2dD+/y33O939H15S/8Pj32T1E0aSoGok/3s3//+A+J/Uv+/v6bX33mO39p23i3zOdvR5ffp2z+o+/y/vS/r/9m/+1d/y7/X//f8fA42f88Y/aJfeL9f/4Uf9/k/v7m54D+fP3k79P3p1A3C+o/5X+nfr36iP+p2+d+/0P3039d+V1D9X+v/X3v046Xf6b5f4y4D7I/5L4jOev//7a5+/X/N++742e3/xzeuS03eK5Of+vCj/bO/H6O/9iUj/i8X/b+nO9x2S3p/q5+l20v8j/7M2xP+O/yHpt1XyI6n7f8271A37+38s2S7S/7L+v9z5+P4/9/X28GvI5v2y6e7U+2M/eR9e88d0+H/+Xl9P3X+t2f+XvP++t/v+9/L3+O4/tLff2aX3v+4zI1v1a5C4R/yfv4m4S+9X/t/G+1/w8d3S292+/rbexJ3f/i4323lvev/+X713eT9S/1O79A7u0uX1+X2e3m/p6X/m0/1a3m11f7/T13e3pde5u5Pn3u313/f7vL1A/9ve/4e4/P52O+/m/3yvL8Dl2d0H0N1v/z3d8c4E8X/iR4v7S4fSfvj8+eY/JOn1p5/+G3Lvd/t+/71ffD8p3v5+T+p20v+9eX/6E4A8367+m5uSvt+/I9I+/+eN/42A//E/X2n3d3T1+/p6erubI/IeEjeI/yS3aX4/oK27X/btdsveDtdsT+/sve7eLqC3xedv53d4er63I91A3x//X0p30O/039/eBfh8O2I7SBy49f872p1/G+zudwVI4/2v9eXp932X9p/X5/X6+v333smd7f8y6dveBbrJ0p339vX2tvd2eXpS9vT3fXfv3s43yXqfJ5+/f19/v6e138fpTfvC3X/44A4+7w73f324x/f3qUjv2NveL42f7y/v3tve23/39uX93e3m7vS0S/P/o7653++S/mP/s1P3A12X/6b/A4kDRNIn5F+kXo2/8pW/XPL/e+/fIe7/qfud5O+/m///0ve3t69vfO+/d+Ld//i2/94/3+v+6NvfU/2fSvsA8YpE/JH2H1+Q/xP1P43InXyM+/s9/X9/3f3+/q2Xer//3ZvvS9uP1A+2JAgS3/ifLpM44vv3vXhA4ghByJ4E4d14X/9//4d6i9Sfe3/pI5I0kiSoFPlp0m/j/4s4f4z8P/xHovs73e7mrfX+i3L3f3737f0+mP//9L5e+/1//S0/SvrL9f+S1A+oP8/33/23u9X/+/4a3f/8O5/0U/E8f9y0/zNf1n+/UfPf9/+P2vOdr3P3t6/19x31/+3v1P/o2+jS+t89/k8//X0yT+p/X3eS/B5s+p8/k/zX298vS/4r/1q94mO3X9m1a5eGfKz6SdLv4p9E9/v+e994R1p//1+2pP5G3/21fUu72v3m7+4n6Xm7eL8P//Mv0v/P//x23fv7/f+O/9/S/4m/65L2//v0f6R//3+L/i8+l406ffA+f7p919fV/OynLwD/+9/S//+cE3+/6f//75//7mbf/7S4/18a2d/743f113aT123kL+/fL9f/S1L/X+4f13/x9039R4n/u4f/8O+0jfrfSvvf+/X/T9eP42s++4u5/p695m//S0v3/33z3/71+2/e3+z0O4XzB9qf/POf373f//j/+776/a9z49O/6b17/8lfnv31l8X/u9a+P533e4yP/U9vfv3//nL//v/3vT2y0U/f3922vX840/x+q6Hff225m/X6f/j6O4D3/3eI9m7aL1H7k3/72sWfvA3M/Mv/3a9/91+a973+n/+U+O+S1P/p8f8X/Hve++j/+8N//f/7//vNff/4L//8D8Sfv70s+Q+1m8f3z+H4/H0s/f/2s138iAfxT+XvfeO7XfK+5L/e/YOfp8T/190v+fXp/u/2/v/kI+2//z8/l9a365u0f25/A50P/6D/v/U///D3v//q2/veI+4/tS73s41a/z9++eY+P/4/X7u/+X/p8n/4z82++3f/1+0L36/v/Uo34Cftv+O/aP/z9N/fT3p/+k6T+S348/++//375/3+P7W20d9p/3P39Xf0xTftm3z+m92vP933x3fA694vPdr0/5bI/w5fX1yT+mG8/f8/77d/E4D/N/Vvf38a+j3qf/34mXpI/Ym6/2f/5X1s+p+/f/9j3x//u9d3/1m5+a//7f9984920n4n1/4bSfyf/wP3R2m3f3+34xO82X342XlA/4eW3h5I/J/4UfXv4qf/f3f00S7k/5+a+/y9vS3p32X3f++b+/203S3kE23f8n9d+211/+lA/sX/1s/3G/Xv9p3/8yX3/1/+9e/5f/8x+3231N0e/n3A/Y/+6//z1X8u3y/y/3/363dO/0uR+Jv5b79eO/23f+j/f/43Uv5f7x3vfe0/++O3/u6f93I+9X/+d33/43Ovv/m9+9//j7x/f2s+/O8mS/5uXpT3d5//+/x0v5e6/3/Ife+/+L++2+I+I/3/sW/3O7z27e69fH9O/797vA/X///o2O+e/2+/4//p23t++J/0+4/S/s9//3X/1/f0/++n/+X8P31/79m0S41f173f32eLd3e/v41b3y3v//L/v///164A49//7l2m/2e5+q33xH39/z9I6U+/0//D/y//x/f3//32+S//5+i3x///66S331n+3+G3/23ffLzff895/982f6f//jN6+/X/183S//r//f1/2P/+3//z3v+nLd32/5eH3H7u34v/8u32824X/v3/9/z7rfe989//4e4f//P292/37t/0H1f39fS+M9+l4f/f3N148s8G8m//uM8D4A80b4I/A+393E2p97A529C5wP8A7YHf3p18+S2i+/r9f05P4x3a19//u9M6f52e/k3S3dvu+b3+e4GzXUD9ffqM32I10N/l3yEfgP32115Sfe3e7vL5On3+9L43431L6/d7A7/O9fUfUHzX3e8I/9fX2+D29054/L8T61xX4e2X4/0E3U//+3eG+S//U//N5evp/yX6m7e7aY20O5q29Xl2eD/9T7w+/qfve9cff+P14//4m32X7v93P3S63m5//S/6S3t9f4O7X+s795N94P7929007tve8y1545L40vR7Ie7m0e3t+9vS/e/98+50/f0yO3pme8+8957u+2/k/e7e6u3S3sO70/3a5e8fud/d7P52+1vA39O252I/5a+/x38+1++71+vfW/64X8C/I8y8X44a33u7+n3b9Xp0eX1s4d/j1d6+f29vfze7u/eO1P/32fX/jvvv0Xo37/T72591+n+x+IuX2/93Ovu9ffre4N94P4P3X53O/+Pve3t3eO++/c6+Xq4/vj9Xff9M1fU/pvdj+1/I/O+L4C/6v++nff2/f4Xf+9eP1/38T60///3X23q6mre3t7i3/I1++j0m5A7xL8xS/X7+z15uD34P2eL+/m/v///3s01A/y/T/v8L9++77e1O6/293S4/rX29vd9e14e1M63e1Of03/X3I3S4/ve427e1/f7///q0m3X/p/+btdvE3x+s9v6W5y+bvf6+/z2B7/2839/i3f1///p/+1//v4m++/9vU7/e8L7350A5351+X///42//5vv++1/m3t2u//4I3f8D3T3d//u6m7xP9/a3c20A101/6///7f///yX+//r7vX/8d1N7t9/9+/71L/X9/qA31/l///X3d/+///pA2e/433v34B892Lp/73X3/8b/P1/3p75/e3v/34x78G852Ld6//e///3//5/18A3n/9v///9e///a5sP//98t///249/X///p//2sN/X//ff3d//f/++/v6/3e4X////+/t//0O/5v//8Xf/+/1/f99f/e///+/2///f+//fX9///7//5+0f/73v9/2////71//93//175/X/74a/+32+f7v39v/1//4C//uD+2D//8/1v6yv/v//+//1v////7x448f8O2H1p3Xb3/X9x/3e52A+/4s3u///sE//+//f7/e4///2s0f3//e6X//40///u4v4/1L////v297///8v3///3338ff4B//Xv/73/v4E///f///r8yX/1v//+S5/9v448eX87x8c//xL81iM//L8A+z/29f8f/x881v4f///50/v/70//2//2/X///u/f/v7e2D/t+/+21980v+//48s8X7/+/iB//z9f//3v/+81v9/2v//z2f7/418a9018eN+74f4/A///e+///z2//s7//79f/5//A/2sU/5w/f+9948X/z///5/33//xL9Xf714A/pA4/eS9m5A///s019+947/7/f37v++sP//4v//m2D/v9/fA/++/y///u//7498c8a///X//f9v9///m8e/s3/+sY//f9v31f47/63X+A+n1p48A//115456f918eOP1548v44d+H8//w415/+/r6/e4e/0//+/sA3///+//3f/+w//pA/12848c/4596d/v74/298A+I35x/z3///+8d9S943eN+64d93P7e///33vvA3A34ffx6f++/r539+/uX//4+x/S/+s9+I35yvv//w4x6//w//v//3f7d///458d3N2p//A/+/++/20n5sI35///20m3X/iX3a///1A3///4b2wB/q/4A++N64d88e4s12xM//5ff+Xp7f/s19v99++/d///j9fX4///vv/9yv+I//r/wSfv8e/L20A175v///uS66479e3O2+eO4w3+3v///0/f++/bS///e15v////9sT////mff+/s98A179+1f//3/f3A6Tz6ff/f//s9/A/eX53///e2Xm4/24s37v/3+9/wA2///79//4G/f+//+/b7m/u///t//s142vv2B5++/b5//z2s4yS/9A4/eS9t+/e4e5X///8m2D/t219/+/5vv++u32+2/c2P/f3Xf5G7u///+4v20f++/3vv///sA2//39e///8w12++/z92/A/dff++sN93O364v/3+/f++/z///+sA18v/8ff++/eX4e/S/++9v448d///9m2u1mN73s30SfvA21/+0m3X/7Sbe1A77t+L/5/v/j6//sB/eX52//s9++/s1/v/+A/Xv5G79/A4w3/9SfvE5f+I/J/9XfL/f81///sX///u4v5///++/vv/4a74v7/f+m////i3++t5p/99++/++/s4e3s3e///+A+/9v//698b/44s6//799++v/6yXm1+/f++/ffvX///+B39/7///3+/s4e/C++S/sA3m865s33+//pS//e+2v6Sfv8a//sJ/e///6y8++/e/+/v4vvE7/eS//s1A/y/++/43w75/e///7y/+4ffzX/+X5//9/7wB31SfvC///t8d/46e4++/5X//+/p9X++/c7v46/eXv6z///+m/c2e///d/X9+/f2f/3d8A1+//f56/9e3s6///23d7++/zX23m48vv/74vv2141///A6eX31899v4x47514y/A///sX2017Sbe///f/60n53////3e1P++8/f8/f403eA++/++/9X7v////9sB3t3A6/X4d//7/8///dffX4e7eA///7A4/++/b1u6X/35vv880b++/3W9f++/9/v219e/++b13A///m/e0vvvv++/+/346764+/b///v/s4/44v0//28y3++t4w340/3+/r++/13v34e80a3A/A+O2x3A3A37v7++/+++78///3+/865A1523yX31A/A57eB/f/A2P/5m1d9X+//70v8w5+G///u1A172vv5/b//+0m3f2XbSbe2vvX//v19vv/x/34m+/+vv19/5u1++/d2Xy9/393+/03310v7S9/332+/++///6x///z3//9vv34e++b///06/s3++/+//A2vv0G7929A3mff403X//+SfvC7z9//7b1+/sN33+P//+/3m8396/m+/34D7/37+/43//3322+d++2e/++/Xv++/f210/1903m881v2P++6//7a//49/5p2/e60m61A7///x/3f7t98v//v///e2X++/w9f+3+741++3S/6/w1/++/1/48083818eNP16y620m3v/6X//p3X3m+61m71A+92v++/e+z++/z5+6v/w++f++/x3+//ffx5e2b3vv7wB++3s739m73s4e+4v8S/a75f/+18817s/X++vv03x4//5//09/48y//ff3f//2/6/+s++/3++/86e3/5f381vv/4B//S35a/eA3A/b++/m+/e++/++/yB/+f8eNP3s303eS/wO+286s6A77+/+M93X06y3e5m5S/9398/1S/36++/X///i/23vS///7wA/5++/bXn///9s8380+/b37++/e/9+06++/00A733y++7W3X36yS3f23i53229b/3u/A36///ff8/+/5f9v9///m2f/94v0/328/0/5+/ff+/x7+63uX03/++/1/d28/+A//7f/s4y///c/9A3y6S3f2m8f+54G5m/4260m64a3m64a2++/C++/1v3//x3//7vv///2sP/A6x1vv4/e2e///S96y1vvf3++/A2//x/v5m9f1+7f3vA2/S4s/e///Xf//b///4S3vv/83e+z4S///A3vX8///X4B2////u7A/f4e41A9y1++/y2///0vvvv/8e54s664/d34++//5/x6++/c2X6x5++/2vvfA2P/+C98w56Xf/+21++/f4++fA+/S////2X0//3vv9vXf///u++/30S5vvA4y5m1++/++/r7e2s0a++/038G35S4///z4A7///+/b2A+/m++/w3v40608vv2Xm1/+/c961A3bA/+M9++/A38/++/9vffs4+++v/u//++/f5+210vv++/++/7a4vvf4S8/+2+++8/9++2///5+2P++/s4yA6++4s20A+/8yS1e25/2X0/S963/27vv/4B4++/sA+/c1///sA2Xy0A64e/U92++/f7///+u9A1++619A5+///94//282f///8w3f35a8f4s80c///x++f861+0A3x/+/f/37++a4++/5s1+0418m173p4z++/89vv9w6++sN0+++01f/3+/++/s3++/d++/++X55///882m++f+/X3++97793//A///+/s4y5m///3++/9u6X19/48++0844f2//22+//A//7+//f/87p+++03/61v/m+/b/1///s6X1S4f1S3e+/A///89u++/u4s6///A//362f//5u1f1+32vv//8A++/S+/S///4X/+3+C//c++/s6/31+G5e///s9+vvfX3n///7y03//7sP89++x6y///8041A41865m3S5m+4v/++/B//+/s1X/8e44e2/9+/5A3///sA69v/498C///S///2S7m33083n7v38//8/35A5y7m///4++/f9s4y///3vv/+dffv6m/++/++z628m4z7w///8x5dff+/f++3/++//a02++/A3f/4a1y//2/93///49A///m2++/8f+/e///0m//s4e3f///3e+/u///v9vv///7+6//55u//r///s0d3C3e6/3/A++/0e/+vX9//423+/9X/+t+/A++/e//9e3v///v9///XvA4/++/b1+5/S///7++/++/u8x5v46X+/A3v0A3//s3///3//5S6X//A7e////d///A43+//v3sA3w7d4/uX2S////B/++/A43+/5+/+++93+/19e1///7+z///9+++///++/m63e6/f/3w7++/++/++w58S8//38//s//S4e///0S////7vv//s0411+389X/39v++/S+2//++/s1+Xvv+//sI8a3X++/A3/f/f0/r3///3///9Xn///9s635fA/+I++A/e++t//8x/++/c3X/S7a3++/+0v/s///5u+/2U3++/86e39///X3++/d8x5m+/+8a23/s3n/+S+/p80y///83x4X/+069s1X/+a7++X++/++/s3s7f4///+z25e2A3832y/f5m1sX+4vv3vv/+3v+/ffXfX/z5++/9e/e++/A2S7S5v9f3vvXwB++9/3/+m+/w5f++/eXffS9a4+/e/b/++/u39/v4S8eS8e///s405S9x18G8394e/03f02vv/s3vvv/zX/v5+/S9a3+/sI++/++/49w18u++/++sO82a/+m0e2/9A+X2v/+0v+++t2/+e3/m3/v15u3/0y/dff0uS++/eXv//201Xvv/++/++S+/90v///f/+/c0v++ffS5014631++/eS/212++/e9y99+++S1++/3e//28/+A//12vv++/++t4//s4y2++/yB///4++/f++/e///S8++/83/Xp4f2x///c89vv/+++7f/++/5s2195v1A+/++/m80a//A6f/30uS2//A5x653e16/8S/a7///z5/+1/00S/1//A6e++/4e/+/w5m//2+m/3/c1A+/b2ffv3s1f9///0m3f2Xb/eX33++/2+/35v1A+/9++/z30A195d//x/f++4e++/++mS8/3nS9/5ffpS7++/c9v980d2vv/s4x2/3s4a2/8zvv0S5u04A3+//v5m++/21A3s8///2/f230e++/802+/++/B8y3++/A180/0675g9y7y3m6m/9e2f/vv++/3S+v++/2S/++/3++/3s3030uC///ff7++/m+/b++/v0u//s3e1A34C7m+/r/vv///vv72+/zX/+2f5m1/++/2++X3m/++3++x7v8y++/2a0b/+m7s1a3+/4f//v4b95f/++/y3++/+/8b/m5++/s41323f//80x3e15+61/S///51vv9/+++/v3s064wB/+8v90m36S267//82v/481m/f/c9/2X435fvv+S7+/++/++d35G++f1A/+2//vvx/Xf8++/8S6++/23m//2ffr773++/5g+4s412A+/m///++/a728Xv3++/w++/+t///b//Xm82+/060719ff//f/4++/4e/+069vv/8X++/f/ff/83A7S+/a198c///w0///2y4A66w32e4d2A6++/6+Xf//6ff3265++/v/x/+3++/7x4++fA++//983/+z++/y+/269A9++/c0m+/18++/ff4a9+/z2+/ff++S/+2/u9++Sff//715u2y0x0m/++/m+/b0++/v/+2Xf9sS/+y2A6wB78++/X3m9sN2/w5yX23++21++/+/2sB/a43X/3/+9A93vv///4f+y8S3A3A+X35v++/c69+2f7S/++/++4B34y+/19+++/S/e/+167m64d3X69yS9S++/0v2A332e++/+++x3+7/u9+/063e++/3///20A+95///+/v+/36X7y3v4fA6x++/++d4v++/A23+//+eS++/1+03///0S++/210/+4Xm/+6X///++sA50v2y7Xffvv5///3/+f/+0v+++3m86x0sB++2v/4G/+3//+y302Xm//8/yX2//++/f///S0A6++/+++6X2/+eXm//sB/e969a/1//6++x++/42y+/96/Xp//m7d/X2eS1e4d/+5A3f/y3u3/sI/x///eS/+2+/f1A+yW///f2/ff3++/vvA6ffv/++/+/9+S9c3y/0vvp389f4b3///82U07x428a2A+/vvS++/X/eS/2sB/a7++/4vvf4S/+Xp9f/t/47p1a88z+/A6f9A5A6S+/63++/X+n/+3s3e2Uvv/yUfX///++/++61mS91f//7u7A528++//73/1S//6e++/802/e+e////1v//596e++/f/0m/1++/ff++z++/4X843A+3s9A53X6w4X6/+9/vA27a4d5A5f26938++/v8w/A/+00A4S8++/77S/++/++N5yA5Xf3532f/y+S/iA/9u3///f++/S/4A+/p/0eX0f0e/X1s8fA17/m++X2++/e8A/A//f31s14y++/35s3++/9/A6++/+//+S5A3fXff3d///A6++/86d/w8u+5/y1+X//+e//22++/82ffp3n2vv++/e8w/+6/++/f4y8x4w340/3eX++/N++/00f86X5A9fvv61m019fA4429vffpX619n++/806++/dff4y80X6+M++/+/w42/a3v5sXv4f//y2/p9S5fX++3S/339A++/3u1x4e++/1vv9e++98/4/7X++/y2+/f0a3//21X//++/b/6x/m/r4f346++/3vv++/A+61m71//v/+s401/e4f21++/X/v8///++/23/5G7f//42y31+/9++/++7f5e/+f09//e0f/t+3sA3wB++/m/eS++/f0e///3///+/e0m++/s01A++0f++m/8X3/49++u5m9sB///+/u/+++0/2ff2m/y+/pA3S9A+/2S8/v0e9m03f02vvn9m18e++/+/ff2140A+/S4p8a18y8X44a8Xf1/+//b7m1e1948x6/++fA3+/019+3vS9a4+/e/b++/ff+C2A5f267v/+S1/8b/6/0vv///2x/5u++/b5vv++eXffv9w///808m3e+z2/+88++/20f++/3//4d++/062S1e4///9++/m5S64Xvvv02ffs3/++/a1m/bXm+/1/f9e++/f7X46fS02///v3++/B10++/b//+/3++/++/++/0f//3w+04e++/sI5++/9v/+U///++/0e3049sA3++/e378v++a233y///y31/+/7++/++d++/9f33A++/f++1vvvv30A4vv/y343/A/3++/2y/+/++/Xff3e0/e+/+/sA1+u++/++S++81f/++/u+3++9e9vv8x4s++/8+///++/v8136x3m/++/s4e/C35u+w7A///u0X0//f1v6///+//8f/++"

# ใช้ Streamlit Layout
with col_preview:
    st.subheader("👁️ ตัวอย่างใบเสร็จรับเงิน (Receipt Preview)")
    
    # ดึงค่า HTML พร้อมแทรกภาพโลโก้ Base64
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap" rel="stylesheet">
    <style>
        @page {{
            size: A4 portrait;
            margin: 10mm;
        }}
        * {{
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Sarabun', sans-serif;
            color: #000;
            margin: 0;
            padding: 5px;
            background-color: #fff;
        }}
        .receipt-box {{
            border: 1.5px solid #000;
            padding: 15px;
            font-size: 13px;
            line-height: 1.35;
            width: 100%;
            max-width: 780px;
            margin: 0 auto;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .border-table, .border-table th, .border-table td {{
            border: 1px solid #000;
        }}
        .btn-print {{
            margin-top: 15px;
            width: 100%;
            max-width: 780px;
            display: block;
            margin-left: auto;
            margin-right: auto;
            background-color: #059669;
            color: white;
            border: none;
            padding: 12px;
            border-radius: 6px;
            font-weight: bold;
            cursor: pointer;
            font-size: 16px;
            font-family: 'Sarabun', sans-serif;
        }}
        @media print {{
            .btn-print {{ display: none !important; }}
            body {{ padding: 0; background: none; }}
            .receipt-box {{ border: 1.5px solid #000; max-width: 100%; }}
        }}
    </style>
    </head>
    <body>

    <div class="receipt-box">
        <div style="text-align: right; font-size: 13px; font-weight: bold; margin-bottom: 6px;"><u>{doc_type}</u></div>

        <table style="margin-bottom: 8px;">
            <tr>
                <td style="width: 32%; vertical-align: top;">
                    <!-- แสดงรูปภาพโลโก้ตรงตามต้นฉบับ -->
                    <img src="{LOGO_BASE64}" style="width: 100%; max-width: 220px; height: auto; display: block;">
                </td>
                <td style="width: 68%; padding-left: 15px; vertical-align: top;">
                    <div style="font-size: 16px; font-weight: bold;">บริษัท เอ แอนด์ เค ทรานสปอร์ต จำกัด</div>
                    <div style="font-size: 15px; font-weight: bold; margin-bottom: 4px;">A & K TRANSPORT CO.,LTD.</div>
                    <div style="font-size: 11px;">สำนักงานใหญ่ : 48/1 หมู่ที่ 3 ซอยใจเอื้อ ต.บางขะแยง อ.เมืองปทุมธานี จังหวัดปทุมธานี 12000</div>
                    <div style="font-size: 11px;">Head Office : 48/1 M00 3, Soi Jaiaoue1 , Bangkayeang, Mangpathumthani, Pathumthani 12000</div>
                    <div style="font-size: 11px;">Tel. 0-2975-3103 fax. 0-2975-3103 เลขประจำตัวผู้เสียภาษี 0135566024644</div>
                </td>
            </tr>
        </table>

        <div style="text-align: right; font-size: 12px; margin-bottom: 4px;"><b>วันที่ / Date :</b> {receipt_date}</div>

        <table class="border-table" style="text-align: center; margin-bottom: 0px;">
            <tr>
                <td style="width: 20%; padding: 4px;">รหัสลูกค้า<br><span style="font-size: 10px;">Customer Code</span></td>
                <td style="width: 40%; padding: 4px;">เงื่อนไขการชำระเงิน<br><span style="font-size: 10px;">Terms of Payment</span></td>
                <td style="width: 20%; padding: 4px;">พนักงานขนส่ง</td>
                <td style="width: 20%; padding: 4px;">เลขที่ใบเสร็จรับเงิน<br><span style="font-size: 10px;">Receipt No.</span></td>
            </tr>
            <tr style="height: 28px;">
                <td>{customer_code}</td>
                <td>{payment_term}</td>
                <td>{driver_name}</td>
                <td style="font-weight: bold;">{receipt_no}</td>
            </tr>
        </table>

        <div style="border: 1px solid #000; border-top: none; padding: 6px 10px; margin-bottom: 0px;">
            <div><b>ชื่อลูกค้า :</b> {cust_name}</div>
            <div><b>ที่อยู่ :</b> {cust_address}</div>
            <div><b>เลขประจำตัวผู้เสียภาษี :</b> {cust_taxid}</div>
        </div>

        <table class="border-table" style="border-top: none;">
            <thead>
                <tr style="text-align: center; background-color: #f9f9f9;">
                    <th style="width: 8%; padding: 5px;">ลำดับที่<br><span style="font-size: 10px; font-weight: normal;">Item</span></th>
                    <th style="width: 42%; padding: 5px;">รายการ<br><span style="font-size: 10px; font-weight: normal;">Description</span></th>
                    <th style="width: 10%; padding: 5px;">จำนวน<br><span style="font-size: 10px; font-weight: normal;">Qty</span></th>
                    <th style="width: 10%; padding: 5px;">หน่วย<br><span style="font-size: 10px; font-weight: normal;">Unit</span></th>
                    <th style="width: 15%; padding: 5px;">ราคา/หน่วย<br><span style="font-size: 10px; font-weight: normal;">Price/Unit</span></th>
                    <th style="width: 15%; padding: 5px;">จำนวนเงิน<br><span style="font-size: 10px; font-weight: normal;">Amount</span></th>
                </tr>
            </thead>
            <tbody>
                <tr style="height: 28px; text-align: center;">
                    <td>1</td>
                    <td style="padding: 2px 8px; text-align: left;">{item_desc}</td>
                    <td>{item_qty}</td>
                    <td>{item_unit}</td>
                    <td style="padding: 2px 8px; text-align: right;">{formatted_price}</td>
                    <td style="padding: 2px 8px; text-align: right;">{formatted_amount}</td>
                </tr>
                <tr style="height: 26px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr style="height: 26px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr style="height: 26px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr style="height: 26px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr style="height: 26px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr style="height: 26px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr style="font-weight: bold;">
                    <td colspan="3" style="padding: 6px 8px; text-align: left;">{text_baht}</td>
                    <td colspan="2" style="padding: 6px; text-align: center;">ยอดสุทธิ</td>
                    <td style="padding: 6px 8px; text-align: right;">{formatted_amount}</td>
                </tr>
            </tbody>
        </table>

        <div style="margin-top: 10px; font-size: 12px; line-height: 1.8;">
            <div><b>ชำระโดย :</b></div>
            <div>{chk_cash} เงินสด ................................................................................................บาท</div>
            <div>{chk_transfer} เงินโอน ................................................................................................บาท</div>
            <div>{chk_cheque} เช็ค &nbsp; ธนาคาร........................................สาขา...........................................................................................</div>
        </div>

        <table class="border-table" style="margin-top: 15px; text-align: center; font-size: 12px;">
            <tr>
                <td style="width: 33%; padding: 8px; vertical-align: top;">
                    <div>ผู้รับเงิน</div><br><br><br>
                    <div>วันที่................................................</div>
                </td>
                <td style="width: 33%; padding: 8px; vertical-align: top;">
                    <div>ผู้รับใบเสร็จ</div><br><br><br>
                    <div>วันที่................................................</div>
                </td>
                <td style="width: 34%; padding: 8px; vertical-align: top;">
                    <div>ในนามบริษัท เอ แอนด์ เค ทรานสปอร์ต จำกัด</div><br><br><br>
                    <div>ประทับตราบริษัท</div>
                </td>
            </tr>
        </table>
    </div>

    <button class="btn-print" onclick="window.print()">🖨️ พิมพ์ใบเสร็จรับเงิน / Save PDF (บาลานซ์ A4)</button>

    </body>
    </html>
    """
    components.html(full_html, height=920, scrolling=True)
