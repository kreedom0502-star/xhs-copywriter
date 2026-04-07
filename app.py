from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# 从环境变量获取API密钥
API_KEY = os.environ.get('MOONSHOT_API_KEY', 'sk-yRV43jRyqPxDxss7jdhK0dhNDhBX3SJqw4QCJbY1Jo0z324q')
API_URL = 'https://api.moonshot.cn/v1/chat/completions'

@app.route('/api/generate', methods=['POST'])
def generate_copy():
    try:
        data = request.json
        
        product_name = data.get('productName', '')
        product_type = data.get('productType', '')
        selling_points = data.get('sellingPoints', '')
        target_audience = data.get('targetAudience', '')
        price_range = data.get('priceRange', '')
        usage_scenario = data.get('usageScenario', '')
        
        if not product_name or not selling_points:
            return jsonify({'error': '产品名称和核心卖点不能为空'}), 400
        
        prompt = f"""你是一位资深的小红书种草文案专家，擅长撰写高转化、高互动的爆款笔记。

【产品信息】
产品名称：{product_name}
产品类型：{product_type or '未指定'}
核心卖点：{selling_points}
目标人群：{target_audience or '未指定'}
价格区间：{price_range or '未指定'}
使用场景：{usage_scenario or '未指定'}

【爆款文案公式 - 必须严格执行】
1. 标题公式：数字+痛点+利益点+情绪词+emoji（例：用了3年耳机才知道😭这款降噪真的太绝了！）
2. 开头公式：3秒钩子 = 具体场景+情绪共鸣（例：每天早上地铁上，那个噪音真的让我崩溃...）
3. 正文公式：真实体验+3个具体细节+1个对比+使用场景描述
4. 结尾公式：互动引导 = 提问/投票/求推荐（例：你们平时通勤都戴什么耳机？评论区聊聊～）
5. 标签公式：3个精准产品标签+2个热门泛标签

【质量要求 - 必须满足】
- 每篇文案500-800字，不能太短
- 每个版本至少使用8个emoji
- 必须包含具体的数字、时间、场景描述
- 语气要像真实用户分享，不能官方腔
- 必须提到产品的具体使用感受

【输出格式 - 严格按此格式】
版本1【真实测评型】
【标题】：（15-25字，含数字和emoji）
【正文】：（开头钩子→产品发现过程→3个具体使用细节→优缺点→购买建议）
【话题标签】：（5个标签，格式#标签）
【封面建议】：（配色+构图+文字排版）
【配图建议】：（需要几张+每张拍什么）

版本2【清单种草型】
【标题】：（15-25字，含数字和emoji）
【正文】：（场景引入→对比表格→推荐理由→避坑指南）
【话题标签】：（5个标签）
【封面建议】：（配色+构图+文字排版）
【配图建议】：（需要几张+每张拍什么）

版本3【反套路型】
【标题】：（15-25字，含数字和emoji）
【正文】：（先抑后扬开头→制造冲突→解释原因→产品解决→效果验证）
【话题标签】：（5个标签）
【封面建议】：（配色+构图+文字排版）
【配图建议】：（需要几张+每张拍什么）

【禁止事项】
- 禁止空话套话（如"真的很不错""值得推荐"）
- 禁止官方宣传口吻
- 禁止每个版本结构雷同
- 禁止字数少于500字"""

        response = requests.post(
            API_URL,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {API_KEY}'
            },
            json={
                'model': 'moonshot-v1-8k',
                'messages': [
                    {
                        'role': 'system',
                        'content': '你是一位专业的小红书文案生成专家，擅长撰写高转化、高互动的种草文案。'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'temperature': 0.5,
                'max_tokens': 3000
            },
            timeout=60
        )
        
        result = response.json()
        generated_text = result['choices'][0]['message']['content']
        
        # 对每个版本进行爆款基因分析
        versions_analysis = analyze_viral_elements(generated_text, product_type)
        
        return jsonify({
            'success': True,
            'data': generated_text,
            'analysis': versions_analysis
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate-cover', methods=['POST'])
def generate_cover():
    try:
        data = request.json
        cover_suggestion = data.get('coverSuggestion', '')
        title = data.get('title', '')
        
        if not cover_suggestion and not title:
            return jsonify({'error': '封面建议或标题不能为空'}), 400
        
        # 构建封面图提示词 - 聚焦排版和氛围，不生成具体产品
        cover_prompt = f"""Xiaohongshu style cover design, vertical 3:4 ratio,
title text overlay area, aesthetic background only,
{cover_suggestion},
NO physical product in image, focus on mood and atmosphere,
clean minimalist layout, soft gradient or textured background,
professional graphic design, highly detailed, 8k"""

        # 构建配图提示词 - 强调场景氛围，弱化具体产品
        image_prompt = f"""Lifestyle scene photography for social media post,
showing usage environment and atmosphere only,
{title}, {cover_suggestion},
focus on scene setting, mood lighting, lifestyle context,
NO close-up product shots, NO specific product details,
realistic ambient lighting, cozy lifestyle setting, high quality, 4k"""

        # 调用Kimi API生成更专业的提示词
        response = requests.post(
            API_URL,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {API_KEY}'
            },
            json={
                'model': 'moonshot-v1-8k',
                'messages': [
                    {
                        'role': 'system',
                        'content': '你是一位专业的AI绘画提示词工程师，擅长生成小红书风格的图片提示词。重要原则：不要生成具体产品外观，而是生成氛围背景和场景环境。'
                    },
                    {
                        'role': 'user',
                        'content': f'''请基于以下文案信息，生成两个AI绘画提示词：

标题：{title}
封面建议：{cover_suggestion}

要求：
1. 封面图提示词：竖版3:4，突出标题排版区域，生成美观的背景氛围图（渐变、纹理、场景氛围），**绝对不能出现具体产品**
2. 配图提示词：生成使用场景的环境氛围图（桌面、房间、户外场景等），**绝对不能出现产品特写或具体产品外观**

两个提示词都要用英文，适合Midjourney/即梦AI。记住：我们只生成背景和氛围，产品需要用户自己拍摄实物图后合成上去。'''
                    }
                ],
                'temperature': 0.7,
                'max_tokens': 2000
            },
            timeout=60
        )
        
        result = response.json()
        ai_content = result['choices'][0]['message']['content']
        
        return jsonify({
            'success': True,
            'data': {
                '封面提示词': cover_prompt,
                '配图提示词': image_prompt,
                'ai优化建议': ai_content,
                '图片生成提示词': cover_prompt,  # 兼容前端
                '使用建议': '提示词生成的图片仅包含背景和氛围，请自行拍摄产品实物图后进行合成。'
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def analyze_viral_elements(text, product_type):
    """分析文案中的爆款基因元素"""
    
    # 爆款元素库
    viral_elements = {
        '标题技巧': {
            '数字': r'\d+',
            'emoji': r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]',
            '痛点词': ['崩溃', '后悔', '踩雷', '绝了', '惊艳', '真香', '救命', '必看'],
            '悬念词': ['没想到', '原来', '才发现', '秘密', '真相'],
            '情绪词': ['哭', '笑', '震惊', '感动', '爱了', '破防']
        },
        '结构元素': {
            '钩子开头': ['你知道吗', '说实话', '坦白', '救命', '家人们'],
            '细节描写': ['具体', '真实', '亲测', '用了', '天'],
            '对比手法': ['之前', '现在', '对比', '区别', 'vs'],
            '互动引导': ['?', '？', '评论', '聊聊', '分享', '你们']
        },
        '爆款公式': {
            '真实测评型': ['亲测', '真实', '体验', '优缺点', '建议'],
            '清单种草型': ['清单', '合集', '盘点', '对比', '推荐'],
            '反套路型': ['不要', '别', '反而', '竟然', '居然']
        }
    }
    
    import re
    
    # 解析三个版本
    versions = []
    version_patterns = [
        (r'版本1.*?【(.*?)】', '版本1'),
        (r'版本2.*?【(.*?)】', '版本2'),
        (r'版本3.*?【(.*?)】', '版本3')
    ]
    
    for pattern, version_name in version_patterns:
        match = re.search(pattern, text)
        if match:
            style = match.group(1)
            # 提取该版本的内容
            start = match.start()
            next_version = text.find('版本' + str(int(version_name[-1])+1), start)
            if next_version == -1:
                version_text = text[start:]
            else:
                version_text = text[start:next_version]
            
            # 分析标题
            title_match = re.search(r'【标题】[：:]\s*(.+?)(?=\n|$)', version_text)
            title = title_match.group(1) if title_match else ''
            
            # 分析正文
            content_match = re.search(r'【正文】[：:]\s*([\s\S]+?)(?=\n【|$)', version_text)
            content = content_match.group(1) if content_match else ''
            
            # 评分计算
            scores = {
                '标题吸引力': 0,
                '结构完整度': 0,
                '互动引导力': 0,
                '真实感': 0
            }
            
            # 标题评分
            title_score = 60  # 基础分
            if re.search(r'\d+', title): title_score += 10  # 有数字
            if re.search(r'[\U0001F600-\U0001F64F]', title): title_score += 10  # 有emoji
            if any(w in title for w in viral_elements['标题技巧']['痛点词']): title_score += 10
            if any(w in title for w in viral_elements['标题技巧']['悬念词']): title_score += 5
            if any(w in title for w in viral_elements['标题技巧']['情绪词']): title_score += 5
            scores['标题吸引力'] = min(title_score, 100)
            
            # 结构评分
            structure_score = 60
            if any(w in content for w in viral_elements['结构元素']['钩子开头']): structure_score += 10
            if any(w in content for w in viral_elements['结构元素']['细节描写']): structure_score += 10
            if any(w in content for w in viral_elements['结构元素']['对比手法']): structure_score += 10
            if any(w in content for w in viral_elements['结构元素']['互动引导']): structure_score += 10
            scores['结构完整度'] = min(structure_score, 100)
            
            # 互动评分
            interaction_score = 60
            if '?' in content or '？' in content: interaction_score += 15
            if any(w in content for w in ['评论', '聊聊', '分享']): interaction_score += 15
            if any(w in content for w in ['你们', '大家', '姐妹']): interaction_score += 10
            scores['互动引导力'] = min(interaction_score, 100)
            
            # 真实感评分
            authentic_score = 60
            if any(w in content for w in ['亲测', '真实', '自己', '我']): authentic_score += 15
            if re.search(r'\d+天|\d+周|\d+个月', content): authentic_score += 15  # 有时间线
            if '缺点' in content or '不足' in content: authentic_score += 10  # 有客观评价
            scores['真实感'] = min(authentic_score, 100)
            
            # 计算总分
            total_score = sum(scores.values()) // 4
            
            # 生成优化建议
            suggestions = []
            if scores['标题吸引力'] < 80:
                suggestions.append('标题可加入数字+痛点词+emoji组合，提升点击率')
            if scores['结构完整度'] < 80:
                suggestions.append('正文可增加具体使用场景和对比细节')
            if scores['互动引导力'] < 80:
                suggestions.append('结尾可加入提问或投票，引导评论互动')
            if scores['真实感'] < 80:
                suggestions.append('可增加个人使用体验时间线和客观优缺点')
            
            # 识别使用的爆款基因
            genes = []
            if re.search(r'\d+', title): genes.append('数字吸睛')
            if re.search(r'[\U0001F600-\U0001F64F]', title): genes.append('emoji情绪')
            if any(w in title for w in viral_elements['标题技巧']['痛点词']): genes.append('痛点共鸣')
            if any(w in content for w in ['亲测', '真实']): genes.append('真实人设')
            if any(w in content for w in ['对比', '之前', '现在']): genes.append('反差对比')
            if '?' in content: genes.append('互动提问')
            
            versions.append({
                'version': version_name,
                'style': style,
                'title': title,
                'scores': scores,
                'total_score': total_score,
                'viral_genes': genes,
                'suggestions': suggestions if suggestions else ['整体质量不错，可尝试发布测试效果']
            })
    
    return versions

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)