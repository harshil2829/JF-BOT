'use server';

import { cookies } from 'next/headers';

export async function loginAction(username, password) {
  // Normalize spaces/formatting to guarantee success (handles whitespaces/pasted inputs)
  const enteredUser = username ? username.trim() : '';
  const enteredPass = password ? password.trim() : '';

  // Support both 'pass 28295609' and raw code '28295609'
  if (enteredUser === 'admin' && (enteredPass === 'pass 28295609' || enteredPass === '28295609')) {
    const cookieStore = await cookies();
    
    // Retrieve appropriate session token hash
    const token = enteredPass === '28295609'
      ? '84b9f72538211113e69f3dcadb53721e1f12a65ac250077808fc2674ae01c0e1'
      : '2faf50e937bdc80f99f88ab7a8d09f45b810eba4d795d9bd51011c307649565e';

    cookieStore.set('jf_session', token, {
      httpOnly: true,
      secure: false, // Disable secure flag to guarantee cookie acceptance on local HTTP dev environments
      sameSite: 'strict',
      maxAge: 60 * 60 * 24, // 1 day session longevity
      path: '/'
    });
    return { success: true };
  }
  return { success: false, error: 'Invalid administrative credentials' };
}

export async function logoutAction() {
  const cookieStore = await cookies();
  cookieStore.delete('jf_session');
  return { success: true };
}
