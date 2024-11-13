import cv2
import numpy as np
import tensorflow as tf

# Cargar el modelo entrenado
model = tf.keras.models.load_model("modelo_vocales.keras")

# Etiquetas de las clases
class_names = ['A', 'E', 'I', 'O', 'U']
confidence_threshold = 0.8  # Umbral de confianza

# Iniciar la cámara
cap = cv2.VideoCapture(0)

while True:
    # Leer imagen de la cámara
    ret, frame = cap.read()
    if not ret:
        print("Error al leer la cámara. Finalizando...")
        break

    # Preprocesar la imagen para el modelo
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertir de BGR a RGB, si el modelo fue entrenado en RGB
    img = cv2.resize(img, (64, 64))               # Redimensionar
    img = img / 255.0                             # Normalizar
    img = np.expand_dims(img, axis=0)             # Añadir dimensión batch

    # Realizar predicción
    predictions = model.predict(img)
    confidence = np.max(predictions)              # Obtener la confianza de la predicción más alta
    if confidence > confidence_threshold:
        predicted_class = class_names[np.argmax(predictions)]
    else:
        predicted_class = "Letra no detectada"

    # Mostrar la predicción en la ventana de video
    cv2.putText(frame, f"Predicción: {predicted_class} (Confianza: {confidence:.2f})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Detección de Vocales", frame)

    # Agregar un pequeño delay para reducir la carga del sistema
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar ventanas
cap.release()
cv2.destroyAllWindows()
