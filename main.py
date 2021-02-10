from time import sleep
from selenium import webdriver
import chromedriver_autoinstaller
from auth.auth import username, passw


def carregar_lista_videos():
    try:
        lista = list()
        with open('videos-lista.txt', 'r') as arq:
            for valor in arq:
                lista.append(valor.replace('\n', ''))
    except FileNotFoundError:
        print('Erro ao localizar o arquivo!')
    finally:
        arq.close()
    return lista


def baixar_video():
    botao_baixar = driver.find_element_by_xpath(
        '//*[@id="main"]/div/main/div/div/div/div[2]/div[2]/div/button[1]/span')
    botao_baixar.click()

    sleep(1)
    while True:
        try:
            # botao_240p = driver.find_element_by_xpath('//*[@id="download_panel"]/div/div[1]/div[2]/a/span')
            driver.find_element_by_xpath('//*[@id="download_panel"]/div/div[1]/div[2]/a/span')
        except SyntaxError:
            sleep(1)
            continue
        else:
            break

    # Botões de Download do vídeo
    try:
        botao_1080p = driver.find_element_by_xpath('//*[@id="download_panel"]/div/div[6]/div[2]/a/span')
        botao_1080p.click()
    except SyntaxError:
        botao_720p = driver.find_element_by_xpath('//*[@id="download_panel"]/div/div[4]/div[2]/a/span')
        botao_720p.click()
    except SyntaxError:
        botao_540p = driver.find_element_by_xpath('//*[@id="download_panel"]/div/div[3]/div[2]/a/span')
        botao_540p.click()


def percorrer_lista():
    lista = carregar_lista_videos()
    for c in lista:
        # Abrindo página do vídeo
        driver.get(c)

        sleep(2)

        try:
            caixa_mensagem_fechar = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/button')
        except SyntaxError:
            baixar_video()
            print(f'Baixando o vídeo: {c}')
        else:
            caixa_mensagem_fechar.click()
            baixar_video()
            print(f'Baixando o vídeo: {c}')


if __name__ == '__main__':
    # Driver
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()

    # Abrindo página do Vimeo
    driver.get('https://vimeo.com/manage/videos')

    # Tipo de login
    tipo_login = int(input('Escolha o tipo de login:\n'
                           '1 - Login manual\n'
                           '2 - Credenciais inseridas no arquivo contrib/auth.py\n'))

    if tipo_login == 2:
        # Autenticação

        campo_user = driver.find_element_by_id('signup_email')
        campo_senha = driver.find_element_by_id('login_password')
        botao_entrar = driver.find_element_by_xpath('//*[@id="login_form"]/div[5]/input')

        campo_user.send_keys(username)
        campo_senha.send_keys(passw)
        botao_entrar.click()
    elif tipo_login == 1:
        input('Entre na sua conta do Vimeo e depois tecle ENTER')

    percorrer_lista()
