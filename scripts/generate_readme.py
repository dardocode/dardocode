# scripts/generate_readme.py
import os
import requests
import json
from datetime import datetime
import random

class ReadmeGenerator:
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        self.username = os.getenv('GITHUB_USERNAME')
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def get_random_dev_quote(self):
        """Obtener una cita aleatoria de programación"""
        quotes = [
            "El código es como el humor. Cuando tienes que explicarlo, es malo. - Cory House",
            "Primero, resuelve el problema. Entonces, escribe el código. - John Johnson",
            "El código limpio siempre parece que fue escrito por alguien a quien le importa. - Robert C. Martin",
            "Cualquier tonto puede escribir código que una computadora pueda entender. Los buenos programadores escriben código que los humanos pueden entender. - Martin Fowler",
            "El debugging es como ser detective en una novela de crimen donde también eres el asesino. - Filipe Fortes"
        ]
        return random.choice(quotes)
    
    def get_weather_emoji(self):
        """Obtener emoji del clima basado en la hora"""
        hour = datetime.now().hour
        if 6 <= hour < 12:
            return "🌅"  # Mañana
        elif 12 <= hour < 18:
            return "☀️"  # Tarde
        elif 18 <= hour < 22:
            return "🌆"  # Atardecer
        else:
            return "🌙"  # Noche
    
    def get_activity_emoji(self):
        """Obtener emoji de actividad basado en el día"""
        day = datetime.now().weekday()
        emojis = ["💻", "🚀", "⚡", "🔥", "✨", "🎯", "🌟"]
        return emojis[day % len(emojis)]
    
    def generate_dynamic_header(self):
        """Generar header dinámico"""
        weather = self.get_weather_emoji()
        activity = self.get_activity_emoji()
        current_time = datetime.now().strftime("%A, %B %d")
        
        return f"""# {weather} ¡Hola! Soy {self.username} {activity}

<div align="center">

![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&duration=3000&pause=1000&color=36BCF7&center=true&vCenter=true&width=435&lines=Desarrollador+Full+Stack;Siempre+aprendiendo+algo+nuevo;{current_time})

</div>

> 💡 **Cita del día:** {self.get_random_dev_quote()}

---"""
    
    def generate_about_section(self):
        """Generar sección 'Sobre mí'"""
        return """
## 🚀 Sobre mí

- 🔭 Actualmente trabajando en proyectos emocionantes
- 🌱 Siempre aprendiendo nuevas tecnologías
- 👯 Abierto a colaboraciones interesantes
- 💬 Pregúntame sobre desarrollo web, APIs, o cualquier cosa tech
- ⚡ Dato curioso: Me encanta resolver problemas complejos con código elegante

<div align="center">

### 🛠️ Mi Stack Tecnológico

![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Python](https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/-React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Node.js](https://img.shields.io/badge/-Node.js-339933?style=for-the-badge&logo=node.js&logoColor=white)
![Git](https://img.shields.io/badge/-Git-F05032?style=for-the-badge&logo=git&logoColor=white)

</div>
"""
    
    def get_github_stats_section(self):
        """Generar sección de estadísticas GitHub"""
        return f"""
<div align="center">

## 📊 Estadísticas de GitHub

<img src="https://github-readme-stats.vercel.app/api?username={self.username}&show_icons=true&theme=radical" alt="GitHub Stats" />

<img src="https://github-readme-streak-stats.herokuapp.com/?user={self.username}&theme=radical" alt="GitHub Streak" />

<img src="https://github-readme-stats.vercel.app/api/top-langs/?username={self.username}&layout=compact&theme=radical" alt="Top Languages" />

</div>
"""
    
    def generate_activity_section(self):
        """Generar sección de actividad"""
        return f"""
## 📈 Actividad Reciente

<!--START_SECTION:activity-->
<!-- Esta sección se actualiza automáticamente -->
<!--END_SECTION:activity-->

<div align="center">

![Contribution Graph](https://github-readme-activity-graph.vercel.app/graph?username={self.username}&theme=radical)

</div>
"""
    
    def generate_projects_section(self):
        """Generar sección de proyectos destacados"""
        return """
## 🎯 Proyectos Destacados

<div align="center">

<!-- Repositorios que se actualizarán automáticamente -->
<a href="https://github.com/anuraghazra/github-readme-stats">
  <img align="center" src="https://github-readme-stats.vercel.app/api/pin/?username={}&repo=repo1&theme=radical" />
</a>
<a href="https://github.com/anuraghazra/convoychat">
  <img align="center" src="https://github-readme-stats.vercel.app/api/pin/?username={}&repo=repo2&theme=radical" />
</a>

</div>
""".format(self.username, self.username)
    
    def generate_contact_section(self):
        """Generar sección de contacto"""
        return f"""
## 🤝 Conecta conmigo

<div align="center">

[![LinkedIn](https://img.shields.io/badge/-LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/{self.username})
[![Twitter](https://img.shields.io/badge/-Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/{self.username})
[![Email](https://img.shields.io/badge/-Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:{self.username}@gmail.com)

### 📊 Visitantes del perfil
![Visitors](https://visitor-badge.glitch.me/badge?page_id={self.username}.{self.username})

</div>
"""
    
    def generate_footer(self):
        """Generar footer con timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        return f"""
---

<div align="center">

### ⚡ "El código es poesía en movimiento" ⚡

*Última actualización automática: {timestamp}*

![Snake animation](https://github.com/{self.username}/{self.username}/blob/output/github-contribution-grid-snake.svg)

</div>
"""
    
    def generate_complete_readme(self):
        """Generar README completo"""
        sections = [
            self.generate_dynamic_header(),
            self.generate_about_section(),
            self.get_github_stats_section(),
            self.generate_activity_section(),
            self.generate_projects_section(),
            self.generate_contact_section(),
            self.generate_footer()
        ]
        
        return '\n'.join(sections)
    
    def save_readme(self):
        """Guardar README generado"""
        try:
            readme_content = self.generate_complete_readme()
            
            with open('README.md', 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            print("✅ README generado exitosamente!")
            print(f"📝 Archivo: README.md")
            print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return True
            
        except Exception as e:
            print(f"❌ Error generando README: {e}")
            return False

if __name__ == "__main__":
    generator = ReadmeGenerator()
    generator.save_readme()
