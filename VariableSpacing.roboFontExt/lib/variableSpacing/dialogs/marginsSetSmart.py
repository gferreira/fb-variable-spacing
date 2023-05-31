from variableSpacing import smartSetMargins
from variableSpacing.extras.hTools3_marginsSet

class SmartSetMarginsDialog(SetMarginsDialog):

    title = 'margins+'
    key = f'{SetMarginsDialog.key}Smart'

    def apply(self):

        # -----------------
        # assert conditions
        # -----------------
        
        font = self.getCurrentFont()
        if not font:
            return

        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return

        if not (self.left or self.right):
            return

        # ----------
        # print info
        # ----------

        if self.verbose:
            print('setting margins smartly:\n')
            print(f'\tleft: {self.modes[self.leftMode]} {self.leftValue} ({self.left})')
            print(f'\tright: {self.modes[self.rightMode]} {self.rightValue} ({self.right})')
            print(f'\tbeam: {self.beamY} ({["OFF", "ON"][int(self.beam)]})')
            print(f'\tglyphs: {", ".join(glyphNames)}')
            print()

        # ----------------
        # transform glyphs
        # ----------------

        leftMargin  = self.leftValue  if self.left  else None
        rightMargin = self.rightValue if self.right else None

        smartSetMargins(font, glyphNames,
                leftMargin=leftMargin, leftMode=self.leftMode,
                rightMargin=rightMargin, rightMode=self.rightMode,
                useBeam=self.beam, beamY=self.beamY)

        # done
        font.changed()
        if self.verbose:
            print('...done.\n')

# -------
# testing
# -------

if __name__ == "__main__":

    from mojo.roboFont import OpenWindow
    SmartSetMarginsDialog()
