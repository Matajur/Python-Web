token = localStorage.getItem('accessToken')


/**
 * The get_contacts function fetches the contacts from the server and displays them in a list.
 * 
 *
 *
 * @return A promise
 *
 * @docauthor Trelent
 */
const get_contacts = async () => {
  const response = await fetch('http://localhost:8000/api/contacts', {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  console.log(response.status, response.statusText)
  if (response.status === 200) {
    result = await response.json()
    contacts.innerHTML = ''
    for (contact of result) {
      el = document.createElement('li')
      el.className = 'list-group-item'
      el.innerHTML = `ID: ${contact.id} Fullname: <b>${contact.name} ${contact.thurname}</b> Email: ${contact.email} Phone: ${contact.phone} Birthday: ${contact.birthday} Notes: ${contact.notes}`
      contacts.appendChild(el)
    }
  }
}


/**
 * The get_next_birthdays function fetches the next birthdays from the API and displays them in a list.
 * 
 *
 *
 * @return A promise
 *
 * @docauthor Trelent
 */
const get_next_birthdays = async () => {
  const response = await fetch('http://localhost:8000/api/contacts/next_birthdays', {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  console.log(response.status, response.statusText)
  if (response.status === 200) {
    result = await response.json()
    next_birthdays.innerHTML = ''
    for (celeb of result) {
      el = document.createElement('li')
      el.className = 'list-group-item'
      el.innerHTML = `ID: ${celeb.id} Fullname: <b>${celeb.name} ${celeb.thurname}</b> Email: ${celeb.email} Phone: ${celeb.phone} Birthday: ${celeb.birthday} Notes: ${celeb.notes}`
      next_birthdays.appendChild(el)
    }
  }
}

get_contacts()
get_next_birthdays()

contactCreate.addEventListener('submit', async (e) => {
  e.preventDefault()
  const response = await fetch('http://localhost:8000/api/contacts', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      name: contactCreate.name.value,
      thurname: contactCreate.thurname.value,
      email: contactCreate.email.value,
      phone: contactCreate.phone.value,
      birthday: contactCreate.birthday.value,
      notes: contactCreate.notes.value,
    }),
  })
  if (response.status === 201) {
    console.log('Contact is created')
    get_contacts()
    get_next_birthdays()
  }
})