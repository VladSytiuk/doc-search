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
            mutation UploadDocumentMutation($file: Upload!, $key: String) {
                uploadDocument(file: $file, key: $key) {
                    success                         
                }
            }
        """

DELETE_DOCUMENT_MUTATION = """
            mutation delete($id: ID) {
              deleteDocument(id: $id) {
                document {
                  id
                }
              }
            }
        """

USER_DOCUMENTS_QUERY = """
                query  {
                  userDocuments{
                    id
                    document
                    owner{
                      username
                    }
                  }
                }
            """

CREATE_KEY_MUTATION = """
            mutation CreateKeyMutation{
              createKey{
                key {
                  key
                  documentsLimit
                  queriesLimit
                  user{
                    username
                  }
                }
              }
            }
        """

USER_KEYS_QUERY = """
            query  {
              userKeys{
                key
                documentsLimit
                queriesLimit
              }
            }
        """

QUESTION_QUERY = """
        query question($question: String, $documentId: Int, $key: String) {
          question(question: $question, documentId: $documentId, key: $key) {
            question
            answer
          }
        }
    """
