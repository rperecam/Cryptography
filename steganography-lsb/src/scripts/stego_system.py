import os
import hashlib
import struct
from typing import Tuple
from PIL import Image
import numpy as np
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


class SteganographyConfig:
    """
    Configuración del sistema de esteganografía

    Parámetros criptográficos y de ocultación optimizados para
    seguridad y capacidad de almacenamiento.
    """
    BITS_PER_CHANNEL = 1      # LSB por canal (imperceptible)
    CHANNELS_USED = 3         # R, G, B
    HEADER_SIZE_BYTES = 4     # 32 bits para longitud payload
    AES_KEY_SIZE = 32         # 256 bits (AES-256)
    NONCE_SIZE = 12           # GCM estándar
    TAG_SIZE = 16             # GCM tag de autenticación
    KDF_ITERATIONS = 100000   # PBKDF2 (protección contra fuerza bruta)
    KDF_SALT_SIZE = 16        # Salt de 128 bits


class CryptoEngine:
    """
    Motor criptográfico - AES-GCM con KDF

    Proporciona cifrado autenticado (confidencialidad + integridad) usando
    AES-256-GCM con derivación de clave robusta mediante PBKDF2-SHA256.

    Atributos:
        salt: Salt único para derivación de clave
        aes_key: Clave AES-256 derivada
        prng_seed: Seed para generador de posiciones aleatorias
    """

    def __init__(self, password: str, salt: bytes = None):
        """
        Inicializa motor criptográfico

        Args:
            password: Contraseña maestra
            salt: Salt para KDF (genera uno nuevo si None)
        """
        if salt is None:
            self.salt = os.urandom(SteganographyConfig.KDF_SALT_SIZE)
        else:
            self.salt = salt

        # Derivar clave AES desde password con PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=SteganographyConfig.AES_KEY_SIZE,
            salt=self.salt,
            iterations=SteganographyConfig.KDF_ITERATIONS,
            backend=default_backend()
        )
        self.aes_key = kdf.derive(password.encode('utf-8'))

        # Derivar seed PRNG desde clave AES (limitado a 32 bits para NumPy)
        seed_bytes = hashlib.sha256(self.aes_key).digest()[:4]  # 4 bytes = 32 bits
        self.prng_seed = int.from_bytes(seed_bytes, 'big') & 0xFFFFFFFF

    def encrypt(self, plaintext: bytes) -> Tuple[bytes, bytes, bytes]:
        """
        Cifra con AES-GCM

        Returns:
            (nonce, ciphertext, tag)
        """
        aesgcm = AESGCM(self.aes_key)
        nonce = os.urandom(SteganographyConfig.NONCE_SIZE)

        # AES-GCM devuelve ciphertext || tag
        ciphertext_and_tag = aesgcm.encrypt(nonce, plaintext, None)

        # Separar ciphertext y tag
        ciphertext = ciphertext_and_tag[:-SteganographyConfig.TAG_SIZE]
        tag = ciphertext_and_tag[-SteganographyConfig.TAG_SIZE:]

        return nonce, ciphertext, tag

    def decrypt(self, nonce: bytes, ciphertext: bytes, tag: bytes) -> bytes:
        """
        Descifra y verifica con AES-GCM

        Raises:
            cryptography.exceptions.InvalidTag: Si la verificación falla
        """
        aesgcm = AESGCM(self.aes_key)

        # AES-GCM espera ciphertext || tag
        ciphertext_and_tag = ciphertext + tag

        plaintext = aesgcm.decrypt(nonce, ciphertext_and_tag, None)
        return plaintext


class LSBSteganography:
    """
    Motor de esteganografía LSB con posiciones aleatorias

    Implementa ocultación de información en los bits menos significativos (LSB)
    de imágenes PNG usando una estrategia híbrida:
    - Header + Salt: posiciones secuenciales (para bootstrap)
    - Payload cifrado: posiciones aleatorias deterministas

    La aleatoriedad se basa en un PRNG con seed derivado de la contraseña,
    garantizando reproducibilidad para decodificación.
    """

    def __init__(self, crypto: CryptoEngine):
        self.crypto = crypto

    def _calculate_capacity(self, image: Image.Image) -> int:
        """Calcula capacidad total en bits"""
        width, height = image.size
        total_pixels = width * height
        return total_pixels * SteganographyConfig.CHANNELS_USED * SteganographyConfig.BITS_PER_CHANNEL

    def _generate_position_pool(self, total_positions: int) -> np.ndarray:
        """
        Genera un pool completo de posiciones permutadas

        Args:
            total_positions: Número total de posiciones disponibles

        Returns:
            Array de todas las posiciones en orden permutado
        """
        return self._generate_position_pool_with_seed(total_positions, self.crypto.prng_seed)

    def _generate_position_pool_with_seed(self, total_positions: int, seed: int) -> np.ndarray:
        """
        Genera un pool completo de posiciones permutadas con un seed específico

        Args:
            total_positions: Número total de posiciones disponibles
            seed: Seed para el generador de números aleatorios

        Returns:
            Array de todas las posiciones en orden permutado
        """
        rng = np.random.RandomState(seed)
        # Generar permutación de todas las posiciones
        positions = np.arange(total_positions)
        rng.shuffle(positions)
        return positions

    def _position_to_pixel_channel(self, position: int, width: int) -> Tuple[int, int, int]:
        """
        Convierte posición global a (x, y, canal)

        Args:
            position: Índice global
            width: Ancho de imagen

        Returns:
            (x, y, channel)
        """
        pixel_idx = position // SteganographyConfig.CHANNELS_USED
        channel = position % SteganographyConfig.CHANNELS_USED

        y = pixel_idx // width
        x = pixel_idx % width

        return x, y, channel

    def _build_payload(self, message: bytes) -> bytes:
        """
        Construye payload completo

        Estructura: [salt(16)] [longitud(4)] [nonce(12)] [tag(16)] [ciphertext]
        """
        # Cifrar mensaje
        nonce, ciphertext, tag = self.crypto.encrypt(message)

        # Longitud total del payload cifrado (nonce + tag + ciphertext)
        payload_length = len(nonce) + len(tag) + len(ciphertext)

        # Construir payload
        payload = (
            self.crypto.salt +
            struct.pack('>I', payload_length) +  # Big-endian 32-bit
            nonce +
            tag +
            ciphertext
        )

        return payload

    def _parse_payload(self, payload: bytes) -> Tuple[bytes, bytes, bytes, bytes]:
        """
        Parsea payload extraído

        Returns:
            (salt, nonce, tag, ciphertext)
        """
        offset = 0

        # Extraer salt
        salt = payload[offset:offset + SteganographyConfig.KDF_SALT_SIZE]
        offset += SteganographyConfig.KDF_SALT_SIZE

        # Extraer longitud
        payload_length = struct.unpack('>I', payload[offset:offset + 4])[0]
        offset += 4

        # Extraer nonce
        nonce = payload[offset:offset + SteganographyConfig.NONCE_SIZE]
        offset += SteganographyConfig.NONCE_SIZE

        # Extraer tag
        tag = payload[offset:offset + SteganographyConfig.TAG_SIZE]
        offset += SteganographyConfig.TAG_SIZE

        # Extraer ciphertext
        ciphertext_length = payload_length - SteganographyConfig.NONCE_SIZE - SteganographyConfig.TAG_SIZE
        ciphertext = payload[offset:offset + ciphertext_length]

        return salt, nonce, tag, ciphertext

    def encode(self, image_path: str, message: bytes, output_path: str) -> dict:
        """
        Oculta mensaje en imagen

        Args:
            image_path: Ruta imagen original
            message: Mensaje a ocultar
            output_path: Ruta imagen de salida

        Returns:
            Estadísticas del proceso
        """
        # Cargar imagen
        img = Image.open(image_path).convert('RGB')
        width, height = img.size
        pixels = np.array(img)

        # Verificar capacidad
        capacity_bits = self._calculate_capacity(img)

        # Construir payload
        payload = self._build_payload(message)
        payload_bits_needed = len(payload) * 8

        # Añadir header de longitud total (para saber cuántos bytes leer)
        total_length = len(payload)
        header = struct.pack('>I', total_length)
        full_payload = header + payload

        total_bits_needed = len(full_payload) * 8

        if total_bits_needed > capacity_bits:
            raise ValueError(
                f"Mensaje demasiado grande. Necesario: {total_bits_needed} bits, "
                f"Disponible: {capacity_bits} bits"
            )

        # Convertir a binario
        payload_binary = ''.join(format(byte, '08b') for byte in full_payload)

        # Estrategia híbrida:
        # - Primeros 20 bytes (header 4 + salt 16) usan posiciones secuenciales
        # - Resto usa posiciones aleatorias

        header_salt_bytes = SteganographyConfig.HEADER_SIZE_BYTES + SteganographyConfig.KDF_SALT_SIZE
        header_salt_bits = header_salt_bytes * 8

        # Posiciones secuenciales para header+salt
        sequential_positions = list(range(header_salt_bits))

        # Posiciones aleatorias para el resto (empezando después de header+salt)
        remaining_bits = total_bits_needed - header_salt_bits
        if remaining_bits > 0:
            position_pool = self._generate_position_pool(capacity_bits)
            # Filtrar posiciones ya usadas y tomar las necesarias
            random_positions = [p for p in position_pool if p >= header_salt_bits][:remaining_bits]
            positions = sequential_positions + random_positions
        else:
            positions = sequential_positions[:total_bits_needed]

        # Insertar bits en LSB
        for i, pos in enumerate(positions):
            x, y, channel = self._position_to_pixel_channel(pos, width)

            # Obtener bit a insertar
            bit = int(payload_binary[i])

            # Modificar LSB
            pixel_value = pixels[y, x, channel]
            # Limpiar LSB y establecer nuevo bit
            new_value = (pixel_value & 0xFE) | bit
            pixels[y, x, channel] = new_value

        # Guardar imagen
        stego_img = Image.fromarray(pixels, 'RGB')
        stego_img.save(output_path, 'PNG')  # PNG para evitar compresión con pérdida

        return {
            'message_bytes': len(message),
            'payload_bytes': len(full_payload),
            'bits_used': total_bits_needed,
            'capacity_bits': capacity_bits,
            'usage_percent': (total_bits_needed / capacity_bits) * 100,
            'positions_count': len(positions)
        }

    def decode(self, image_path: str, password: str) -> bytes:
        """
        Extrae mensaje de imagen

        Args:
            image_path: Ruta imagen esteganografiada
            password: Contraseña para descifrar

        Returns:
            Mensaje descifrado
        """
        # Cargar imagen
        img = Image.open(image_path).convert('RGB')
        width, height = img.size
        pixels = np.array(img)

        capacity_bits = self._calculate_capacity(img)

        # PASO 1: Extraer header + salt usando posiciones secuenciales
        # (mismo método que en encode)
        header_salt_bytes = SteganographyConfig.HEADER_SIZE_BYTES + SteganographyConfig.KDF_SALT_SIZE
        header_salt_bits = header_salt_bytes * 8

        # Posiciones secuenciales
        sequential_positions = list(range(header_salt_bits))

        # Extraer bits de header+salt
        header_salt_bits_list = []
        for pos in sequential_positions:
            x, y, channel = self._position_to_pixel_channel(pos, width)
            pixel_value = pixels[y, x, channel]
            header_salt_bits_list.append(pixel_value & 1)

        # Convertir a bytes
        header_salt_binary = ''.join(str(bit) for bit in header_salt_bits_list)
        header_salt_bytes_data = bytes(int(header_salt_binary[i:i+8], 2) for i in range(0, len(header_salt_binary), 8))

        # Extraer header y salt
        header_bytes = header_salt_bytes_data[:SteganographyConfig.HEADER_SIZE_BYTES]
        salt = header_salt_bytes_data[SteganographyConfig.HEADER_SIZE_BYTES:]

        total_payload_length = struct.unpack('>I', header_bytes)[0]

        # PASO 2: Recrear crypto con el salt extraído
        crypto_with_salt = CryptoEngine(password, salt)

        # PASO 3: Calcular bits totales necesarios
        total_bits_needed = (SteganographyConfig.HEADER_SIZE_BYTES + total_payload_length) * 8

        if total_bits_needed > capacity_bits:
            raise ValueError(f"Payload corrupto: requiere {total_bits_needed} bits, capacidad {capacity_bits}")

        # PASO 4: Generar posiciones para el resto del payload
        remaining_bits = total_bits_needed - header_salt_bits

        if remaining_bits > 0:
            position_pool = self._generate_position_pool_with_seed(capacity_bits, crypto_with_salt.prng_seed)
            # Filtrar posiciones ya usadas y tomar las necesarias
            random_positions = [p for p in position_pool if p >= header_salt_bits][:remaining_bits]
            all_positions = sequential_positions + random_positions
        else:
            all_positions = sequential_positions[:total_bits_needed]

        # Extraer todos los bits
        extracted_bits = []
        for pos in all_positions:
            x, y, channel = self._position_to_pixel_channel(pos, width)
            pixel_value = pixels[y, x, channel]
            extracted_bits.append(pixel_value & 1)

        # Convertir a bytes
        binary_string = ''.join(str(bit) for bit in extracted_bits)
        extracted_bytes = bytes(int(binary_string[i:i+8], 2) for i in range(0, len(binary_string), 8))

        # Saltar header y parsear payload
        payload = extracted_bytes[SteganographyConfig.HEADER_SIZE_BYTES:]
        salt_check, nonce, tag, ciphertext = self._parse_payload(payload)

        # Verificar que el salt extraído coincide
        if salt != salt_check:
            raise ValueError("Salt no coincide. Imagen corrupta o contraseña incorrecta.")

        # Descifrar y verificar
        try:
            plaintext = crypto_with_salt.decrypt(nonce, ciphertext, tag)
            return plaintext
        except Exception as e:
            raise ValueError(f"Descifrado fallido. Contraseña incorrecta o imagen corrupta: {e}")


