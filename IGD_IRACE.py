import os
import sys
import time
import shlex
import subprocess
from PyQt5.QtWidgets import *







class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interfaz de Generación de Documentos IRACE")
        self.setGeometry(100, 100, 600, 400)

        # Creamos un widget principal para la ventana
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Creamos un layout vertical principal
        main_layout = QVBoxLayout(main_widget)

        # Creamos un QTabWidget para organizar en pestañas
        tab_widget = QTabWidget()

        # Creamos la pestaña "Requisitos"
        requirements_tab = QWidget()
        tab_widget.addTab(requirements_tab, "Requisitos")

        # Creamos un layout vertical para la pestaña "Requisitos"
        requirements_layout = QVBoxLayout(requirements_tab)

        # Agregar el mensaje indicado
        label_requirements_message = QLabel("Esta herramienta ayuda a la generación de los archivos necesarios para la librería IRACE\n\nSi estás interesado en conocer más sobre esta librería, dirígete a su sitio oficial en internet:")
        label_requirements_message_2 = QLabel("<b>https://cran.r-project.org/web/packages/irace/index.html<\b>")
        label_requirements_message_3 = QLabel("Es obligatorio contar con R e IRACE instalado, además de las variables de entorno en el .bashrc\n\nSi estos conceptos no te son familiares, contactame o lee el manual en la sección \"3. Installation\".")

        requirements_layout.addWidget(label_requirements_message)
        requirements_layout.addWidget(label_requirements_message_2)
        requirements_layout.addWidget(label_requirements_message_3)

        # Creamos la pestaña "Parámetros"
        parameters_tab = QWidget()
        tab_widget.addTab(parameters_tab, "Parámetros")

        # Creamos un layout vertical para la pestaña "Parámetros"
        parameters_layout = QVBoxLayout(parameters_tab)

        # Botón para seleccionar archivo
        self.button_select = QPushButton("Seleccionar template")
        self.button_select.setToolTip("Selecciona el archivo .py ")  # Agregar globo de texto
        self.button_select.clicked.connect(self.open_file_dialog)
        parameters_layout.addWidget(self.button_select)

        # Botón para ejecutar "irace --init"
        self.button_execute = QPushButton("Generar archivos de IRACE")
        self.button_execute.setToolTip("irace --init ")
        self.button_execute.clicked.connect(self.execute_irace_init)
        parameters_layout.addWidget(self.button_execute)

        # Campo de entrada para el número de variables (Tabla 1)
        self.integer_variable = 0
        self.label_variable = QLabel("Número de parámetros de tipo entero y continuo: ", self)
        self.label_variable.setToolTip("# parámetros entero y continuo. Ingresa un número entero.")
        parameters_layout.addWidget(self.label_variable)
        self.line_edit_variable = QLineEdit(str(self.integer_variable), self)
        self.line_edit_variable.textChanged.connect(self.update_integer_variable)
        parameters_layout.addWidget(self.line_edit_variable)

        # Creamos la tabla para ingresar variables y sus rangos (Tabla 1)
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Variable", "Mínimo", "Máximo", "Continuas (r) o Enteras (i)"])
        parameters_layout.addWidget(self.table_widget)

        # Campo de entrada para el número de filas de la tabla 2
        self.integer_values = ""
        self.label_values = QLabel("Número de parámetros de tipo discreto: ", self)
        self.label_values.setToolTip("# parametros discretos. Ingresa un número entero.")
        parameters_layout.addWidget(self.label_values)
        self.line_edit_values = QLineEdit(self.integer_values, self)
        self.line_edit_values.textChanged.connect(self.generate_table_2_auto)  # Conexión para generar automáticamente la tabla 2
        parameters_layout.addWidget(self.line_edit_values)

        # Creamos la segunda tabla (inicialmente oculta)
        self.table_widget_2 = QTableWidget(self)
        self.table_widget_2.setColumnCount(2)
        self.table_widget_2.setHorizontalHeaderLabels(["Variable", "Valores"])
        self.table_widget_2.setVisible(False)
        parameters_layout.addWidget(self.table_widget_2)

        # Botón para añadir parámetros (Tabla 1)
        self.button_add_params = QPushButton("Añadir en parameters.txt")
        self.button_add_params.clicked.connect(self.add_parameters)
        parameters_layout.addWidget(self.button_add_params)

        # Creamos la pestaña "Instancias"
        instances_tab = QWidget()
        tab_widget.addTab(instances_tab, "Instancias")

        # Creamos un layout vertical para la pestaña "Instancias"
        instances_layout = QVBoxLayout(instances_tab)

        # Botón para seleccionar carpeta
        self.button_select_folder = QPushButton("Seleccionar carpeta de instancias")
        self.button_select_folder.setToolTip("En donde se encuentran las instancias")
        self.button_select_folder.clicked.connect(self.open_folder_dialog)
        instances_layout.addWidget(self.button_select_folder)

        # Campo de entrada para el número de filas de la tabla en "Instancias"
        self.label_instance_rows = QLabel("Número de instancias:")
        self.label_instance_rows.setToolTip("# instancias. Agrega nombres textuales de instancias. Ingresa un número entero.")
        instances_layout.addWidget(self.label_instance_rows)
        self.line_edit_instance_rows = QLineEdit()
        instances_layout.addWidget(self.line_edit_instance_rows)

        # Tabla para la pestaña "Instancias"
        self.table_widget_instances = QTableWidget()
        instances_layout.addWidget(self.table_widget_instances)

        # Botón para guardar instancias en archivo
        self.button_save_instances = QPushButton("Escribir en instances-list.txt")
        self.button_save_instances.setToolTip("Guarda las instancias de la tabla. Cuidado con los nombres!")
        self.button_save_instances.clicked.connect(self.add_instances_to_file)
        instances_layout.addWidget(self.button_save_instances)

        # Botón para escribir en scenario.txt
        self.button_write_to_scenario = QPushButton("Escribir en scenario.txt")
        self.button_write_to_scenario.setToolTip("Escribir lineas restantes del scenario.txt")
        self.button_write_to_scenario.clicked.connect(self.write_to_scenario)
        instances_layout.addWidget(self.button_write_to_scenario)

        # Conectar la señal textChanged al campo de entrada para actualizar automáticamente la tabla
        self.line_edit_instance_rows.textChanged.connect(self.update_table_instances)

        # Agregamos el QTabWidget al layout principal
        main_layout.addWidget(tab_widget)

        # Creamos la pestaña "Target - Runner"
        target_runner_tab = QWidget()
        tab_widget.addTab(target_runner_tab, "Target - Runner")

        # Creamos un layout vertical para la pestaña "Target - Runner"
        target_runner_layout = QVBoxLayout(target_runner_tab)

        # Agregar el mensaje indicado
        label_target_runner_message = QLabel("En la linea 37 y 39 del documento target-runner escribe las siguientes instrucciones:\n\nEXE=\"./template.py\"\n\nEXE_PARAMS=\"$INSTANCE  ${CONFIG_PARAMS} ${SEED}\"")
        label_target_runner_message_1 = QLabel("Agrega a template.py de python la siguiente instrucción: #!/usr/bin/env python3")
        label_target_runner_message_2 = QLabel("Podrías usar otro nombre para tu archivo, solo considera que en lugar de \"template.py\" \n\ndebe ir el nombre de tu ejecutable de python")
        label_target_runner_message_3 = QLabel("Los parámetros del ejecutable deben ser pasados con \"sys.argv\" a python.")
        
        target_runner_layout.addWidget(label_target_runner_message)
        
        line_separator = QFrame()
        line_separator.setFrameShape(QFrame.HLine)
        line_separator.setFrameShadow(QFrame.Sunken)
        line_separator.setStyleSheet("color: rgba(169, 169, 169, 0.5);")
        target_runner_layout.addWidget(line_separator)        
        
        target_runner_layout.addWidget(label_target_runner_message_1)

        line_separator = QFrame()
        line_separator.setFrameShape(QFrame.HLine)
        line_separator.setFrameShadow(QFrame.Sunken)
        line_separator.setStyleSheet("color: rgba(169, 169, 169, 0.5);")
        target_runner_layout.addWidget(line_separator)        
        

        target_runner_layout.addWidget(label_target_runner_message_2)

        line_separator = QFrame()
        line_separator.setFrameShape(QFrame.HLine)
        line_separator.setFrameShadow(QFrame.Sunken)
        line_separator.setStyleSheet("color: rgba(169, 169, 169, 0.5);")
        target_runner_layout.addWidget(line_separator)  
        target_runner_layout.addWidget(label_target_runner_message_3)

        self.selected_file = ""
        self.selected_folder = ""

        # Creamos la pestaña "Terminar Escenario"
        finish_scenario_tab = QWidget()
        tab_widget.addTab(finish_scenario_tab, "Terminar Escenario")

        # Creamos un layout vertical para la pestaña "Terminar Escenario"
        finish_scenario_layout = QVBoxLayout(finish_scenario_tab)

        # Campo de entrada para maxExperiments
        label_max_experiments = QLabel("Número máximo de experimentos:")
        label_max_experiments.setToolTip("Ingresa número entero")
        finish_scenario_layout.addWidget(label_max_experiments)
        self.line_edit_max_experiments = QLineEdit()
        finish_scenario_layout.addWidget(self.line_edit_max_experiments)

        # Campo de entrada para parallel
        label_parallel = QLabel("Realizar el proceso en paralelo (Si = 1, No = 0):")
        label_parallel.setToolTip("Preferentemente asignar 1")
        finish_scenario_layout.addWidget(label_parallel)
        self.line_edit_parallel = QLineEdit()
        finish_scenario_layout.addWidget(self.line_edit_parallel)

        # Campo de entrada para digits
        label_digits = QLabel("Cantidad de decimales:")
        label_digits.setToolTip("Número de dígitos a usar para los parámetros. Ingresa número entero.")
        finish_scenario_layout.addWidget(label_digits)
        self.line_edit_digits = QLineEdit()
        finish_scenario_layout.addWidget(self.line_edit_digits)

        # Botón para actualizar scenario.txt
        button_update_scenario = QPushButton("Finalizar scenario.txt")
        button_update_scenario.setToolTip("Terminar de configurar el archivo scenario.txt")
        button_update_scenario.clicked.connect(self.update_scenario_file)
        finish_scenario_layout.addWidget(button_update_scenario)

        main_layout.addWidget(tab_widget)

        # Agregar la pestaña "RUN"
        run_tab = QWidget()
        tab_widget.addTab(run_tab, "Run")

        # Crear un layout vertical para la pestaña "RUN"
        run_layout = QVBoxLayout(run_tab)
        
        button_start_optimization = QPushButton("Optimizar!")

        label_start_message = QLabel("El resultado de la optimización se encontrará en el archivo \"Salida_optimizacion.txt\".")
        label_start_message_2 = QLabel("Considera únicamente el conjunto de parámetros de la parte final del archivo.")
        label_start_message_3 = QLabel("No cierres la terminal hasta que el proceso termine.")
        run_layout.addWidget(label_start_message)
        run_layout.addWidget(label_start_message_3)
        run_layout.addWidget(label_start_message_2)
        
        # Conectar la señal clicked del botón a la función para ejecutar la optimización
        button_start_optimization.clicked.connect(self.start_optimization)       

        # Crear el botón "EMPEZAR OPTIMIZACION"
        run_layout.addWidget(button_start_optimization) 


        # Creamos la pestaña "Reset"
        reset_tab = QWidget()
        tab_widget.addTab(reset_tab, "Reset")

        # Creamos un layout vertical para la pestaña "Reset"
        reset_layout = QVBoxLayout(reset_tab)
        reset_msg = QLabel("En caso de haber cometido un error, deberemos de ejecutar la herramienta de nuevo.\n\nNecesitamos eliminar los archivos generados que tienen informacion incorrecta.")
        reset_msg_2 = QLabel("Al hacer click en Resetear Archivos, se reiniciará esta herramienta\n\ntendrá que escribir cada una de las pestañas")
        reset_layout.addWidget(reset_msg)
        reset_layout.addWidget(reset_msg_2)

        # Agregamos un botón para resetear los archivos
        reset_button = QPushButton("Resetear Archivos")
        reset_button.setToolTip("Eliminar los archivos generados")
        reset_button.clicked.connect(self.reset_files)
        reset_layout.addWidget(reset_button)


        pestanas = [requirements_layout, parameters_layout, instances_layout, target_runner_layout, finish_scenario_layout, run_layout]

        # Agregar los mensajes "Desarrollado por Aarón López ;)" y "Hola" al final de cada pestaña
        for layout in pestanas:
            message_layout = QHBoxLayout()  # Layout horizontal para los mensajes
            message_left = QLabel("<i>Aarón López</i>")
            message_left.setStyleSheet("color: gray;")
            message_layout.addWidget(message_left)
            message_layout.addStretch(1)  # Estirar el espacio entre los mensajes
            message_right = QLabel("<i>jose.portillo@cimat.mx</i>")
            message_right.setStyleSheet("color: gray;")
            message_layout.addWidget(message_right)
            layout.addLayout(message_layout)  # Agregar el layout horizontal al layout de la pestaña

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo", "", "Todos los archivos (*);;Archivos de texto (*.txt)", options=options)
        if file_name:
            print("Plantillaa seleccionada:", file_name)
            self.selected_file = file_name
            os.system(f'chmod +x "{file_name}"')

    def open_folder_dialog(self):
        folder_name = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta")
        if folder_name:
            print("Carpeta seleccionada:", folder_name)
            self.selected_folder = folder_name
            quoted_folder_path = f'"{self.selected_folder}"'
            command_0 = f"echo 'execDir = \"./\"' >> scenario.txt"
            os.system(command_0)
            command = f"echo 'trainInstancesDir = {quoted_folder_path}' >> scenario.txt"
            os.system(command)
            print(f"Línea agregada al final del archivo con: trainInstancesDir = {quoted_folder_path}")

    def execute_irace_init(self):
        if self.selected_file:
            directory = os.path.dirname(self.selected_file)
            os.chdir(directory)
            os.system('irace --init')
            
        else:
            print("No se ha seleccionado ningún archivo.")

    def update_integer_variable(self):
        try:
            new_value = int(self.line_edit_variable.text())
            if new_value >= 0:
                self.integer_variable = new_value
                self.update_table_rows()
        except ValueError:
            pass

    def update_table_rows(self):
        current_rows = self.table_widget.rowCount()
        new_rows = self.integer_variable
        if new_rows > current_rows:
            self.table_widget.setRowCount(new_rows)
            for row in range(current_rows, new_rows):
                for col in range(self.table_widget.columnCount()):
                    item = QTableWidgetItem()
                    self.table_widget.setItem(row, col, item)
        elif new_rows < current_rows:
            self.table_widget.setRowCount(new_rows)

    def generate_table_2_auto(self):
        try:
            num_rows = int(self.line_edit_values.text())
            self.generate_table_2(num_rows)
        except ValueError:
            pass

    def generate_table_2(self, num_rows):
        # Limpiar la tabla 2
        self.table_widget_2.clearContents()
        self.table_widget_2.setRowCount(0)

        # Agregar las filas a la tabla 2
        self.table_widget_2.setRowCount(num_rows)
        for row in range(num_rows):
            for col in range(self.table_widget_2.columnCount()):
                item = QTableWidgetItem()
                self.table_widget_2.setItem(row, col, item)

        # Mostrar la tabla 2
        self.table_widget_2.setVisible(True)

    def add_parameters(self):
        if self.selected_file:
            with open("parameters.txt", "w") as f:
                self.add_parameters_from_table(self.table_widget, f)
                if self.table_widget_2.isVisible():
                    self.add_parameters_from_table_2(self.table_widget_2, f)

            print("Parámetros añadidos al archivo 'parameters.txt'")
        else:
            print("No se ha seleccionado ningún archivo.")

    def add_parameters_from_table(self, table_widget, file):
        for row in range(table_widget.rowCount()):
            variable = table_widget.item(row, 0).text()
            min_value = table_widget.item(row, 1).text()
            max_value = table_widget.item(row, 2).text()
            r_or_z = table_widget.item(row, 3).text()
            file.write(f"{variable} \"\" {r_or_z} ({min_value}, {max_value})\n")

    def add_parameters_from_table_2(self, table_widget, file):
        for row in range(table_widget.rowCount()):
            variable = table_widget.item(row, 0).text()
            values = table_widget.item(row, 1).text().split(',')
            values_str = ", ".join(values)
            file.write(f"{variable} \"\" c ({values_str})\n")

    def update_table_instances(self):
        try:
            num_rows = int(self.line_edit_instance_rows.text())
            self.create_table_instances()
        except ValueError:
            pass

    def create_table_instances(self):
        try:
            num_rows = int(self.line_edit_instance_rows.text())
            self.table_widget_instances.setRowCount(num_rows)
            self.table_widget_instances.setColumnCount(1)
            self.table_widget_instances.setHorizontalHeaderLabels(["Instancias"])
            self.table_widget_instances.show()
        except ValueError:
            print("Ingrese un número entero válido para el número de filas.")

    def add_instances_to_file(self):
        if self.selected_file:
            instances_file_path = os.path.join(os.path.dirname(self.selected_file), "instances-list.txt")
            with open(instances_file_path, "w") as instances_file:
                self.write_instances_to_file(instances_file)
            print("Instancias añadidas al archivo 'Instances.txt'")
        else:
            print("No se ha seleccionado ningún archivo.")

    def write_instances_to_file(self, instances_file):
        for row in range(self.table_widget_instances.rowCount()):
            instance = self.table_widget_instances.item(row, 0).text()
            instances_file.write(f"{instance}\n")

    def write_to_scenario(self):
        if self.selected_file:
            scenario_file_path = os.path.join(os.path.dirname(self.selected_file), "scenario.txt")
            with open(scenario_file_path, "a") as scenario_file:
                # scenario_file.write("execDir = \"./\"\n")
                scenario_file.write("parameterFile = \"./parameters.txt\"\n")
                scenario_file.write("trainInstancesFile = \"instances-list.txt\"\n")
                scenario_file.write("logFile = \"./irace.Rdata\"\n")
            print("Expresiones escritas en 'scenario.txt'")
        else:
            print("No se ha seleccionado ningún archivo.")

    def update_scenario_file(self):
        max_experiments = self.line_edit_max_experiments.text()
        parallel = self.line_edit_parallel.text()
        digits = self.line_edit_digits.text()

        if self.selected_file:
            scenario_file_path = os.path.join(os.path.dirname(self.selected_file), "scenario.txt")
            with open(scenario_file_path, "a") as scenario_file:
                scenario_file.write(f"maxExperiments = {max_experiments}\n")
                scenario_file.write(f"parallel = {parallel}\n")
                scenario_file.write(f"digits = {digits}\n")
            print("Valores agregados a 'scenario.txt'")
        else:
            print("No se ha seleccionado ningún archivo.")

    def start_optimization(self):
        # Ejecutar el comando en la terminal
        os.system('irace >> Salida_optimizacion.txt')
        print("Optimización iniciada. Verifique el archivo 'Salida_optimizacion.txt'")

    def reset_files(self):
        files_to_delete = ["scenario.txt", "target-runner", "configurations.txt", "forbidden.txt", "instances-list.txt", "parameters.txt"]
        for file_name in files_to_delete:
            if os.path.exists(file_name):
                os.remove(file_name)
                print(f"Archivo {file_name} eliminado.")
            else:
                print(f"El archivo {file_name} no existe.")

        print("Reiniciando la aplicación...\n\n")
        self.close()
        time.sleep(1)
        os.system('clear')
        os.system("python3 IGD_IRACE.py")

if __name__ == "__main__":
    subprocess.call(['pip', 'install', 'pyqt5'])
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
