# scripts/update_stats.py
import os
import requests
import json
from datetime import datetime, timedelta
import re

class GitHubStatsUpdater:
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        self.username = os.getenv('GITHUB_USERNAME')
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def get_user_stats(self):
        """Obtener estadísticas del usuario de GitHub"""
        url = f'https://api.github.com/users/{self.username}'
        response = requests.get(url, headers=self.headers)
        return response.json() if response.status_code == 200 else None
    
    def get_repositories(self):
        """Obtener repositorios del usuario"""
        url = f'https://api.github.com/users/{self.username}/repos'
        params = {'per_page': 100, 'sort': 'updated', 'direction': 'desc'}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json() if response.status_code == 200 else []
    
    def get_recent_activity(self):
        """Obtener actividad reciente"""
        url = f'https://api.github.com/users/{self.username}/events/public'
        params = {'per_page': 10}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json() if response.status_code == 200 else []
    
    def calculate_stats(self):
        """Calcular estadísticas interesantes"""
        repos = self.get_repositories()
        stats = {
            'total_repos': len(repos),
            'total_stars': sum(repo['stargazers_count'] for repo in repos),
            'total_forks': sum(repo['forks_count'] for repo in repos),
            'languages': {},
            'most_starred_repo': None,
            'recent_repos': []
        }
        
        # Encontrar el repo más popular
        if repos:
            stats['most_starred_repo'] = max(repos, key=lambda x: x['stargazers_count'])
            stats['recent_repos'] = repos[:5]  # 5 repos más recientes
        
        # Contar lenguajes
        for repo in repos:
            if repo['language']:
                lang = repo['language']
                stats['languages'][lang] = stats['languages'].get(lang, 0) + 1
        
        return stats
    
    def generate_readme_section(self, stats):
        """Generar sección de estadísticas para el README"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Top 5 lenguajes
        top_languages = sorted(stats['languages'].items(), key=lambda x: x[1], reverse=True)[:5]
        
        section = f"""
<!-- STATS_START -->
## 📊 Mis Estadísticas de GitHub

<div align="center">

![Estadísticas de GitHub](https://github-readme-stats.vercel.app/api?username={self.username}&show_icons=true&theme=radical)

</div>

### 🏆 Resumen
- 📁 **Repositorios totales:** {stats['total_repos']}
- ⭐ **Stars totales:** {stats['total_stars']}
- 🍴 **Forks totales:** {stats['total_forks']}

### 💻 Lenguajes más usados
"""
        
        for lang, count in top_languages:
            section += f"- **{lang}:** {count} repositorios\n"
        
        if stats['most_starred_repo']:
            repo = stats['most_starred_repo']
            section += f"""
### 🌟 Repositorio más popular
**[{repo['name']}]({repo['html_url']})** - ⭐ {repo['stargazers_count']} stars
> {repo['description'] or 'Sin descripción'}
"""
        
        section += f"""
### 📈 Repositorios recientes
"""
        
        for repo in stats['recent_repos'][:3]:
            section += f"- **[{repo['name']}]({repo['html_url']})** - {repo['description'] or 'Sin descripción'}\n"
        
        section += f"""
---
*Última actualización: {current_time} UTC*
<!-- STATS_END -->
"""
        
        return section
    
    def update_readme(self):
        """Actualizar el archivo README.md"""
        try:
            # Leer README actual
            with open('README.md', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Calcular estadísticas
            stats = self.calculate_stats()
            
            # Generar nueva sección
            new_section = self.generate_readme_section(stats)
            
            # Reemplazar sección existente o agregar al final
            pattern = r'<!-- STATS_START -->.*?<!-- STATS_END -->'
            if re.search(pattern, content, re.DOTALL):
                # Reemplazar sección existente
                updated_content = re.sub(pattern, new_section.strip(), content, flags=re.DOTALL)
            else:
                # Agregar al final
                updated_content = content + '\n' + new_section
            
            # Escribir README actualizado
            with open('README.md', 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print("✅ README actualizado con nuevas estadísticas!")
            return True
            
        except Exception as e:
            print(f"❌ Error actualizando README: {e}")
            return False

if __name__ == "__main__":
    updater = GitHubStatsUpdater()
    updater.update_readme()
