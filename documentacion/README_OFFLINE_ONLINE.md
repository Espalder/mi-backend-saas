# Sistema de Gestión Empresarial - Modo Offline/Online

## ¿Qué hace esta versión?
- Permite trabajar con la base de datos en la nube (Railway) si tienes internet.
- Si no tienes internet, trabaja automáticamente en modo offline usando una base de datos local (`offline_backup.db`).
- Cuando vuelve la conexión, **sincroniza automáticamente** todos los cambios hechos offline a la nube.
- Muestra un indicador visual del modo actual (online/offline) en la esquina superior derecha.

---

## ¿Cómo instalar y ejecutar?

1. **Instala Python 3.8 o superior**
2. **Instala las dependencias:**
   ```
   pip install -r requirements.txt
   ```
3. **Ejecuta el sistema:**
   ```
   python sistema_gestion_mejorado_modulos/main_offline.py
   ```

---

## ¿Cómo funciona el modo offline/online?
- Al iniciar, el sistema detecta si puede conectarse a la base de datos en la nube.
- Si hay internet, trabajas en la nube (Railway).
- Si no hay internet, trabajas en local (SQLite). Todo lo que hagas se guarda en `offline_backup.db`.
- Cuando vuelve la conexión, el sistema sincroniza automáticamente los datos locales a la nube y te avisa.

---

## ¿Cómo actualizar desde una versión anterior?
1. **Reemplaza la carpeta `sistema_gestion_mejorado_modulos`** por la nueva versión (o solo los archivos modificados si lo prefieres).
2. **(Opcional)** Si tienes datos locales importantes, haz una copia de tu archivo `offline_backup.db` antes de reemplazar nada.
3. **Asegúrate de tener el archivo `requirements.txt` actualizado** y ejecuta `pip install -r requirements.txt` si es necesario.
4. **Ejecuta el sistema normalmente con `main_offline.py`.**

---

## ¿Qué archivos compartir?
- La carpeta `sistema_gestion_mejorado_modulos` completa.
- El archivo `requirements.txt`.
- (Opcional) El archivo `offline_backup.db` si quieres compartir datos locales.
- Este archivo `README_OFFLINE_ONLINE.md` para que todos sepan cómo funciona.

---

## Recomendaciones
- Siempre ejecuta el sistema desde `main_offline.py` para aprovechar el modo offline/online.
- Si trabajas sin internet, no te preocupes: ¡todo se sincroniza cuando vuelva la conexión!
- Si tienes dudas o errores, revisa el mensaje de sincronización o consulta este README.

---

**¡Listo! Ahora puedes compartir el sistema y todos tendrán la versión con modo offline/online y sincronización automática.** 