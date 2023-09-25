CREATE_USER_MUTATION = """
                mutation CreateUserMutation($username: String, $email: String, $password: String) {
                    createUser(username: $username, email: $email, password: $password) {
                        user {
                          username
                          email
                          firstName
                          lastName
                        }
                      }
                    }
                """

USERS_LIST_QUERY = """
          query userslist {
             allUsers {
               id
               username
               email
               firstName
               lastName
            }
          }
        """

UPDATE_PROFILE_MUTATION = """
                mutation UpdateProfileMutation($firstName: String, $email: String, $lastName: String) {
                    updateUser(firstName: $firstName, email: $email, lastName: $lastName) {
                        user {
                          id
                          username
                          firstName
                          lastName
                          email
                        }
                      }
                    }
                """

CHANGE_PASSWORD_MUTATION = """
                    mutation ChangePasswordMutation($oldPassword: String, $newPassword: String) {
                      changePassword(oldPassword: $oldPassword, newPassword: $newPassword) {
                        user {
                          id
                          username
                          firstName
                          lastName
                          email
                        }
                      }
                    }
                """

DELETE_PROFILE_MUTATION = """
                    mutation DeleteProfileMutation($password: String) {
                      deleteProfile(password: $password) {
                        user {
                          id
                          username
                          firstName
                          lastName
                          email
                        }
                      }
                    }
                """

TOKEN_AUTH = """
        mutation TokenAuth($username: String!, $password: String!) {
          tokenAuth(username: $username, password: $password) {
            token
            refreshToken
          }
        }
    """

UPLOAD_DOCUMENT_MUTATION = """
            mutation UploadDocumentMutation($file: Upload!, $key: String!) {
                            uploadDocument(file: $file, key: $key) {
                                document{
                                  title
                                  owner{
                                    username
                                  }
                                }
                             }
                            }
                        """