#!/usr/bin/ruby
print "content-type:text/html\r\n\r\n" 
puts '<!DOCTYPE html>'
puts '<html lang="en">'
puts 
puts '<head>'
puts '  <meta charset="UTF-8">'
puts '  <meta name="viewport" content="width=device-width, initial-scale=1.0">'
puts '  <title>Televised</title>'
puts '  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">'
puts '  <link rel="stylesheet" href="Televised.css">'
puts '<script>'
puts '  console.log("Quicker than the human eye!");'
puts '  userNameNotOKFlag = localStorage.getItem("FalseFlag");'
puts '  console.log(userNameNotOKFlag);'
puts '  console.log("The clock strikes 13....");'
puts '  if (userNameNotOKFlag=="true") {'
puts '     showCreateAccountModal();'
puts '  }'
puts
puts '    document.getElementById("discBtn").addEventListener("click", function(event) {'
puts '      alert("You must be signed in to access Discover.");'
puts '    });'
puts '    </script>'

puts '</head>'
puts 
puts '<body>'
puts '  <nav class="navbar navbar-expand-lg" id="navBar">'
puts '    <div class="container-fluid">'
#puts '      <a class="navbar-brand" href="Home.cgi">'
puts '      <a class="navbar-brand" href="index.cgi">'
puts '        <h2>Televised</h2>'
puts '      </a>'
puts '      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"'
puts '        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">'
puts '        <span class="navbar-toggler-icon"></span>'
puts '      </button>'
puts '      <div class="collapse navbar-collapse" id="navbarSupportedContent">'
puts '        <ul class="navbar-nav mb-2 mb-lg-0">'
puts '          <li class="nav-item">'
puts '            <a class="nav-link active" aria-current="page" href="./">Home</a>'
puts '          </li>'
puts '          <li class="nav-item">'
puts '            <a class="nav-link" href="#" id="createAcc">Create Account</a>'
puts '          </li>'
puts '          <li class="nav-item">'
puts '            <a class="nav-link" href="#" id="SignIn">Sign In</a>'
puts '          </li>'
puts '          <li class="nav-item">'
puts '            <a class="nav-link" href="#" id="discBtn">Discover</a>'
puts '          </li>'
puts '        </ul>'
puts '      </div>'
puts '    </div>'
puts '  </nav>'
puts 
puts '  <!-- Create Account Modal -->'
puts '  <div class="modal fade" id="CreateAccount" tabindex="-1" aria-labelledby="createAccountLabel" aria-hidden="true">'
puts '    <div class="modal-dialog">'
puts '      <div class="modal-content">'
puts '        <div class="modal-header">'
puts '          <h5 class="modal-title" id="createAccountLabel">Create Account</h5>'
puts '          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>'
puts '        </div>'
puts '        <div class="modal-body">'
puts '          <form id="createAccountForm" name="createAccountForm" method="POST" action="createAcc.cgi" onsubmit="return validateAccountCreation();">'
puts '            <div class="mb-3">'
puts '              <label for="unameCreateInput" class="form-label">Username</label>'
puts '              <input type="text" class="form-control" id="unameCreateInput" name="unameCreateInput" placeholder="Enter your username" required>'
puts '              <p style="text-align: right; color: white; font-size: 18px;">Username must be a valid email</p>'
puts '            </div>'
puts '            <div class="mb-3">'
puts '              <label for="passCreateInput" class="form-label">Password</label>'
puts '              <input type="password" class="form-control" id="passCreateInput" name="passCreateInput" placeholder="Enter your password" required>'
puts '              <p style="text-align: right; color: white; font-size: 18px;">Required: 1 capital letter, number, and a special character, min. 12 characters</p>'
puts '            </div>'
puts '            <div class="mb-3">'
puts '              <label for="passConfirm" class="form-label">Confirm Password</label>'
puts '              <input type="password" class="form-control" id="passConfirm" placeholder="Confirm your password" required>'
puts '              <input type="hidden" id="attemptingCreate" name="attempting" value="false">'
puts '              <input type="hidden" id="fromCreate" name="fromCreate" value="true">';
puts '            </div>'
puts '            <div class="modal-footer">'
puts '              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>'
puts '              <button type="submit" class="btn btn-primary" id="createBtn">Create Account</button>'
puts '            </div>'
puts '          </div>'
puts '          </form>'
puts '        </div>'
puts '    </div>'
puts '  </div>'
puts 
puts '  <!-- Sign In Modal -->'
puts '  <div class="modal fade" id="signIn" tabindex="-1" aria-labelledby="SignInLabel" aria-hidden="true">'
puts '    <div class="modal-dialog">'
puts '    <div class="modal-dialog">'
puts '      <div class="modal-content">'
puts '        <div class="modal-header">'
puts '          <h5 class="modal-title" id="signInLabel">Sign In</h5>'
puts '          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>'
puts '        </div>'
puts '        <div class="modal-body">'
puts '          <form id="signInForm" name="signInForm" method="POST" action="createAcc.cgi"">'
puts '            <div class="mb-3">'
puts '              <label for="unameSignInInput" class="form-label">Username</label>'
puts '              <input type="text" class="form-control" id="unameSignInInput" name="unameSignInInput" placeholder="Enter your username" required>'
puts '            </div>'
puts '            <div class="mb-3">'
puts '              <label for="passSignInInput" class="form-label">Password</label>'
puts '              <input type="password" class="form-control" id="passSignInInput" name="passSignInInput" placeholder="Enter your password" required>'
puts '              <input type="hidden" id="attemptingLogIn" name="attempting" value="true">'
puts '              <input type="hidden" id="fromCreate2" name="fromCreate" value="false">'
puts '            </div>'
puts '            <div class="modal-footer">'
puts '              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>'
puts '              <button type="submit" class="btn btn-primary" id="signInBtn">Sign In</button>'
puts '            </div>'
puts '          </div>'
puts '          </form>'
puts '        </div>'
puts '    </div>'
puts '  </div>'



puts '  <!-- Scripts -->'
puts '  <script src="fetch-data-loader.js"></script>'
puts '  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
puts '  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'

puts '</body>'
puts 
puts '</html>'
