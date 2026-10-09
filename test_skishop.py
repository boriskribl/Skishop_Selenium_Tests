import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# lokalna adresa sajta
BASE_URL = "http://localhost/ski_shop"

# podesavanje i pokretanje browsera pre svih testova
@pytest.fixture(scope="module")
def setup():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit() # gasenje drajvera na kraju

# 1. test: provera logovanja na sistem
def test_login_autentifikacija(setup):
    driver = setup
    driver.get(f"{BASE_URL}/login.php")
    
    try:
        # cekamo da se ucita polje za email (u PHP-u je name="email")
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        # polje za lozinku se zove name="lozinka"
        password_input = driver.find_element(By.NAME, "lozinka")
        # dugme nema ime, pronalazimo ga po tipu
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        # unos ispravnih test podataka iz tvog koda
        email_input.send_keys("admin@skishop.com")
        password_input.send_keys("password123")
        login_button.click()
        
        # admin se preusmerava na admin.php prema tvom PHP kodu
        WebDriverWait(driver, 10).until(EC.url_contains("admin.php"))
        assert "admin.php" in driver.current_url
    except Exception as e:
        pytest.fail(f"Prijava neuspesna: {str(e)}")

# 2. test: pretraga ski opreme
def test_pretraga_opreme(setup):
    driver = setup
    # Pretraga se zapravo nalazi na pocetnoj stranici (index.php)
    driver.get(f"{BASE_URL}/index.php")
    
    try:
        # pronalazimo polje za pretragu (name="pretraga")
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "pretraga"))
        )
        search_box.send_keys("Atomic")
        
        # Dugme nema name atribut, pronalazimo ga po tipu unutar forme
        search_button = driver.find_element(By.CSS_SELECTOR, "form button[type='submit']")
        search_button.click()
        
        # Ocekujemo da se prikazu kartice sa rezultatima (umesto html tabele)
        kartica = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "card"))
        )
        assert kartica.is_displayed()
    except Exception as e:
        pytest.fail(f"Pretraga neuspesna: {str(e)}")

# 3. test: provera tabele u admin panelu
def test_admin_panel_prikaz_korisnika(setup):
    driver = setup
    driver.get(f"{BASE_URL}/admin_korisnici.php")
    
    try:
        # admin bi trebalo da vidi tabelu sa registrovanim korisnicima
        tabela_korisnika = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        assert tabela_korisnika.is_displayed()
    except Exception as e:
        pytest.fail(f"Pristup korisnicima neuspesan: {str(e)}")

# 4. test: provera forme za dodavanje opreme
def test_dodavanje_opreme_forma(setup):
    driver = setup
    driver.get(f"{BASE_URL}/oprema_dodaj.php")
    
    try:
        # proveravamo da li korisnik vidi osnovna polja forme
        naziv_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "naziv"))
        )
        cena_input = driver.find_element(By.NAME, "cena")
        
        assert naziv_input.is_displayed()
        assert cena_input.is_displayed()
    except Exception as e:
        pytest.fail(f"Prikaz forme za dodavanje neuspesan: {str(e)}")
