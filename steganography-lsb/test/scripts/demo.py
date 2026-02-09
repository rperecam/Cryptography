#!/usr/bin/env python3
"""
Script de Demostración - Sistema de Esteganografía
Ejemplos prácticos de uso del sistema
"""

import os
from PIL import Image
import numpy as np
from stego_system import CryptoEngine, LSBSteganography


def create_sample_image(output_path: str, width: int = 800, height: int = 600) -> str:
    """
    Crea una imagen de muestra con textura realista

    Args:
        output_path: Ruta donde guardar la imagen
        width: Ancho en píxeles
        height: Alto en píxeles

    Returns:
        Ruta de la imagen creada
    """
    print(f"[+] Creando imagen de muestra ({width}x{height})...")
    
    # Crear array con gradiente de cielo y tierra
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Gradiente de cielo (mitad superior)
    sky_height = height // 2
    sky_gradient = np.linspace(135, 255, sky_height).reshape(-1, 1)
    img_array[:sky_height, :, 2] = sky_gradient  # Canal azul
    img_array[:sky_height, :, 0] = (sky_gradient * 0.7).astype(np.uint8)  # Poco rojo

    # Textura de tierra (mitad inferior) - vectorizado para mejor rendimiento
    earth_height = height - sky_height
    x_coords = np.arange(width)
    y_coords = np.arange(sky_height, height)

    # Generar textura pseudo-aleatoria usando broadcasting
    noise = ((x_coords[np.newaxis, :] * 7 + y_coords[:, np.newaxis] * 13) % 40 - 20)
    green_base = np.linspace(100, 180, earth_height).reshape(-1, 1)

    img_array[sky_height:, :, 1] = np.clip(green_base + noise, 0, 255).astype(np.uint8)  # Verde
    img_array[sky_height:, :, 0] = np.clip(green_base // 2 + noise, 0, 255).astype(np.uint8)  # Rojo
    img_array[sky_height:, :, 2] = np.clip(green_base // 3 + noise, 0, 255).astype(np.uint8)  # Azul

    # Guardar imagen
    img = Image.fromarray(img_array, 'RGB')
    img.save(output_path, 'PNG')
    
    capacity_bytes = (width * height * 3) // 8 - 100
    print(f"[✓] Imagen creada: {output_path}")
    print(f"    Capacidad estimada: ~{capacity_bytes:,} bytes\n")

    return output_path


def demo_basic_usage() -> None:
    """
    Ejecuta la demostración principal del sistema de esteganografía.

    Proceso:
    1. Lee mensaje desde secret_document.txt
    2. Solicita contraseña al usuario
    3. Crea imagen cover y oculta el mensaje cifrado
    4. Extrae y verifica el mensaje
    5. Genera análisis completo (visual, estadístico, capacidad)
    6. Guarda todos los resultados en stego-results/
    """
    print("="*70)
    print("  SISTEMA DE ESTEGANOGRAFÍA - Mensaje Personalizado")
    print("="*70 + "\n")
    
    # Crear carpeta de resultados
    results_dir = "stego-results"
    os.makedirs(results_dir, exist_ok=True)
    print(f"[+] Carpeta de resultados: {results_dir}/\n")

    # Leer mensaje desde archivo
    message_file = "files/secret_document_ex.txt"
    if not os.path.exists(message_file):
        print(f"[✗] Error: No se encuentra el archivo '{message_file}'")
        print(f"    Por favor, crea este archivo en el directorio actual con tu mensaje secreto.")
        return

    with open(message_file, "rb") as f:
        secret_message_bytes = f.read()

    secret_message = secret_message_bytes.decode('utf-8', errors='replace')

    print(f"[+] Mensaje cargado desde '{message_file}':")
    print(f"    Tamaño: {len(secret_message_bytes)} bytes")
    print(f"    Líneas: {secret_message.count(chr(10)) + 1}")
    print(f"    Vista previa:")
    preview_lines = secret_message.split('\n')[:3]
    for line in preview_lines:
        print(f"      {line[:70]}")
    if len(secret_message) > 200:
        print(f"      ...")
    print()

    # Solicitar contraseña al usuario
    print("[+] Ingresa la contraseña para cifrar el mensaje:")
    password = input("    Contraseña: ").strip()

    if not password:
        print("[✗] Error: La contraseña no puede estar vacía")
        return

    print(f"    ✓ Contraseña configurada ({len(password)} caracteres)\n")

    # Crear imagen
    cover_image = create_sample_image(os.path.join(results_dir, "cover_image.png"), 800, 600)

    # Configurar sistema
    crypto = CryptoEngine(password)
    stego = LSBSteganography(crypto)
    
    # Ocultar mensaje
    stego_path = os.path.join(results_dir, "stego_image.png")
    print("[+] Ocultando mensaje cifrado en imagen...")
    stats = stego.encode(
        os.path.join(results_dir, "cover_image.png"),
        secret_message_bytes,
        stego_path
    )
    
    print(f"[✓] Mensaje ocultado exitosamente!")
    print(f"    Archivo: {stego_path}")
    print(f"    Bits usados: {stats['bits_used']:,}/{stats['capacity_bits']:,}")
    print(f"    Capacidad utilizada: {stats['usage_percent']:.2f}%")
    print(f"    Posiciones aleatorias: {stats['positions_count']:,}")
    print()
    
    # Extraer mensaje
    print("[+] Extrayendo mensaje de imagen...")
    recovered_message = stego.decode(stego_path, password)
    recovered_text = recovered_message.decode('utf-8', errors='replace')

    # Guardar mensaje recuperado
    recovered_path = os.path.join(results_dir, "mensaje_recuperado.txt")
    with open(recovered_path, "wb") as f:
        f.write(recovered_message)

    # Verificación
    messages_match = recovered_message == secret_message_bytes
    print(f"[✓] Mensaje extraído y guardado!")
    print(f"    Archivo: {recovered_path}")
    print(f"    Verificación: {'✓ IDÉNTICO AL ORIGINAL' if messages_match else '✗ CORRUPTO'}")
    print()
    
    # Análisis visual detallado
    print("[+] Análisis Visual:")
    cover_img = Image.open(os.path.join(results_dir, "cover_image.png"))
    stego_img = Image.open(stego_path)

    cover_pixels = np.array(cover_img)
    stego_pixels = np.array(stego_img)
    
    diff = np.abs(cover_pixels.astype(int) - stego_pixels.astype(int))

    print(f"    - Diferencia máxima: {diff.max()} (imperceptible)")
    print(f"    - Diferencia promedio: {diff.mean():.6f}")
    print(f"    - Píxeles modificados: {np.sum(diff > 0):,} de {diff.size:,}")
    print(f"    - Porcentaje modificado: {(np.sum(diff > 0) / diff.size * 100):.4f}%")

    # Crear imagen de diferencia (amplificada para visualización)
    diff_amplified = np.clip(diff * 50, 0, 255).astype(np.uint8)
    diff_img = Image.fromarray(diff_amplified)
    diff_path = os.path.join(results_dir, "diferencia_visual.png")
    diff_img.save(diff_path)
    print(f"    - Mapa de diferencias guardado: {diff_path}")
    print()

    # Análisis estadístico por canal
    print("[+] Análisis Estadístico por Canal:")
    for i, color in enumerate(['Rojo', 'Verde', 'Azul']):
        cover_channel = cover_pixels[:, :, i]
        stego_channel = stego_pixels[:, :, i]

        # LSB analysis
        cover_lsb = cover_channel & 1
        stego_lsb = stego_channel & 1

        cover_lsb_ones = int(np.sum(cover_lsb))
        stego_lsb_ones = int(np.sum(stego_lsb))
        total_pixels = cover_lsb.size

        print(f"    Canal {color}:")
        print(f"      - Cover LSB=1: {cover_lsb_ones:,}/{total_pixels:,} ({cover_lsb_ones/total_pixels*100:.2f}%)")
        print(f"      - Stego LSB=1: {stego_lsb_ones:,}/{total_pixels:,} ({stego_lsb_ones/total_pixels*100:.2f}%)")
        print(f"      - Cambio: {abs(stego_lsb_ones - cover_lsb_ones):,} píxeles ({abs(stego_lsb_ones - cover_lsb_ones)/total_pixels*100:.4f}%)")
    print()

    # Métricas de calidad
    print("[+] Métricas de Calidad:")
    mse = np.mean((cover_pixels.astype(float) - stego_pixels.astype(float)) ** 2)
    if mse > 0:
        psnr = 10 * np.log10(255**2 / mse)
    else:
        psnr = float('inf')

    print(f"    - MSE (Mean Squared Error): {mse:.6f}")
    print(f"    - PSNR (Peak Signal-to-Noise Ratio): {psnr:.2f} dB")
    print(f"    - Interpretación: {'Excelente (imperceptible)' if psnr > 40 else 'Buena' if psnr > 30 else 'Detectable'}")
    print()

    # Análisis de capacidad
    print("[+] Análisis de Capacidad:")
    print(f"    - Capacidad total: {stats['capacity_bits']:,} bits ({stats['capacity_bits']//8:,} bytes)")
    print(f"    - Payload original: {len(secret_message_bytes):,} bytes")
    print(f"    - Payload con cifrado: {stats['payload_bytes']:,} bytes")
    print(f"    - Overhead de cifrado: {stats['payload_bytes'] - len(secret_message_bytes):,} bytes")
    print(f"    - Espacio libre restante: {(stats['capacity_bits'] - stats['bits_used'])//8:,} bytes")
    print()

    # Guardar informe completo
    report_path = os.path.join(results_dir, "informe_completo.txt")
    with open(report_path, "w", encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("INFORME COMPLETO - SISTEMA DE ESTEGANOGRAFÍA LSB\n")
        f.write("=" * 70 + "\n\n")

        f.write(f"Fecha: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Archivo de mensaje: {message_file}\n")
        f.write(f"Contraseña: {'*' * len(password)}\n\n")

        f.write("ARCHIVOS GENERADOS:\n")
        f.write(f"  - Imagen cover: cover_image.png\n")
        f.write(f"  - Imagen stego: stego_image.png\n")
        f.write(f"  - Mensaje recuperado: mensaje_recuperado.txt\n")
        f.write(f"  - Mapa diferencias: diferencia_visual.png\n\n")

        f.write("ESTADÍSTICAS DE OCULTACIÓN:\n")
        f.write(f"  - Tamaño mensaje original: {len(secret_message_bytes):,} bytes\n")
        f.write(f"  - Tamaño payload cifrado: {stats['payload_bytes']:,} bytes\n")
        f.write(f"  - Overhead cifrado: {stats['payload_bytes'] - len(secret_message_bytes):,} bytes\n")
        f.write(f"  - Bits utilizados: {stats['bits_used']:,} / {stats['capacity_bits']:,}\n")
        f.write(f"  - Capacidad usada: {stats['usage_percent']:.2f}%\n")
        f.write(f"  - Posiciones aleatorias: {stats['positions_count']:,}\n\n")

        f.write("ANÁLISIS VISUAL:\n")
        f.write(f"  - Diferencia máxima: {diff.max()}\n")
        f.write(f"  - Diferencia promedio: {diff.mean():.6f}\n")
        f.write(f"  - Píxeles modificados: {np.sum(diff > 0):,} de {diff.size:,}\n")
        f.write(f"  - Porcentaje modificado: {(np.sum(diff > 0) / diff.size * 100):.4f}%\n\n")

        f.write("MÉTRICAS DE CALIDAD:\n")
        f.write(f"  - MSE: {mse:.6f}\n")
        f.write(f"  - PSNR: {psnr:.2f} dB\n\n")

        f.write("VERIFICACIÓN:\n")
        f.write(f"  - Mensaje recuperado correctamente: {'SÍ' if messages_match else 'NO'}\n")
        f.write(f"  - Bytes recuperados: {len(recovered_message):,}\n")
        f.write(f"  - Integridad: {'100%' if messages_match else 'CORRUPTO'}\n\n")

        f.write("ANÁLISIS POR CANAL:\n")
        for i, color in enumerate(['Rojo', 'Verde', 'Azul']):
            cover_channel = cover_pixels[:, :, i]
            stego_channel = stego_pixels[:, :, i]
            cover_lsb = cover_channel & 1
            stego_lsb = stego_channel & 1
            cover_lsb_ones = int(np.sum(cover_lsb))
            stego_lsb_ones = int(np.sum(stego_lsb))
            total_pixels = cover_lsb.size

            f.write(f"  Canal {color}:\n")
            f.write(f"    - Cover LSB=1: {cover_lsb_ones:,}/{total_pixels:,} ({cover_lsb_ones/total_pixels*100:.2f}%)\n")
            f.write(f"    - Stego LSB=1: {stego_lsb_ones:,}/{total_pixels:,} ({stego_lsb_ones/total_pixels*100:.2f}%)\n")
            f.write(f"    - Cambio: {abs(stego_lsb_ones - cover_lsb_ones):,} píxeles\n\n")

    print(f"[✓] Informe completo guardado: {report_path}\n")
    print("="*70)
    print("RESUMEN DE ARCHIVOS GENERADOS:")
    print("="*70)
    print(f"📁 {results_dir}/")
    print(f"  📄 cover_image.png          - Imagen original")
    print(f"  📄 stego_image.png          - Imagen con mensaje oculto")
    print(f"  📄 mensaje_recuperado.txt   - Mensaje extraído")
    print(f"  📄 diferencia_visual.png    - Mapa de diferencias")
    print(f"  📄 informe_completo.txt     - Análisis detallado")
    print("="*70 + "\n")


# Funciones auxiliares removidas - solo se usa demo_basic_usage()


def main():
    """Ejecuta la demostración con mensaje personalizado"""
    print("\n" + "="*70)
    print("  SISTEMA DE ESTEGANOGRAFÍA LSB CON AES-GCM")
    print("  Mensaje Personalizado con Análisis Completo")
    print("="*70 + "\n")
    
    try:
        demo_basic_usage()

        print("\n[✓] Proceso completado exitosamente!")
        print("    Revisa la carpeta 'stego-results/' para ver todos los archivos generados.\n")

    except KeyboardInterrupt:
        print("\n\n[!] Proceso interrumpido por el usuario.")
    except Exception as e:
        print(f"\n[✗] Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
