from IPython.display import Javascript
import uuid

class PDBEmbed(object):
    """Embeds pdb and repr as GLmol canvas."""

    def __init__(self, pdb_string, repr_string):
        """Init from given pdb and repr."""
        self.pdb_string = pdb_string
        self.repr_string = repr_string

    def generate_id(self):
        return "glmod_%i" % uuid.uuid4()

    @classmethod
    def quote_js_multiline_string(cls, source_string):
        return "'" + '\' + \'\\n\' + \''.join(l for l in source_string.split("\n") if l) + "'"

    pdb_textarea_template = """
        <textarea  wrap="off" id="%(embed_id)s_src" style="display:none;">
        %(pdb_string)s
        </textarea>
        """
    
    repr_textarea_template = """
        <textarea  wrap="off" id="%(embed_id)s_rep" style="display:none;">
        %(repr_string)s
        </textarea>
        """
    
    display_js_template = """
        element.append('<div id="%(embed_id)s" style="width: auto; height:10in"></div>');

        console.log("Created elements.");
        container.show();


        element.append(%(pdb_textarea)s);
        element.append(%(repr_textarea)s);


        var %(embed_id)s = new GLmol('%(embed_id)s', true);

        console.log("Loaded GLmol as id: %(embed_id)s.");

        function defineRep()
          {
              this.colorByAtom(this.getAllAtoms());
              this.parseRep(this.modelGroup, $('#%(embed_id)s_rep').val());
          }

        %(embed_id)s.rebuildScene = function (repressDraw)
          {
              var time = new Date();

              this.initializeScene();
              this.defineRepresentation();

              console.log("Built scene in " + (new Date() - time) + "ms");

              this.zoomInto(this.getAllAtoms())
              
              if (repressDraw)
              {
                return;
              }
              else
              {
                this.show();
              }
          };

        %(embed_id)s.defineRepresentation = defineRep;
        %(embed_id)s.loadMolecule(true);

        $.data(element.children()[0], "glmol", %(embed_id)s)
        """

    def _repr_javascript_(self):
        """docstring for _repr_javascript"""

        embed_id = self.generate_id()

        pdb_textarea = self.pdb_textarea_template % dict(embed_id = embed_id, pdb_string = self.pdb_string)
        repr_textarea = self.repr_textarea_template % dict(embed_id = embed_id, repr_string = self.repr_string)

        display_js = self.display_js_template % dict(
                embed_id = embed_id,
                pdb_textarea = self.quote_js_multiline_string(pdb_textarea),
                repr_textarea = self.quote_js_multiline_string(repr_textarea))

        return Javascript(display_js, lib = "files/embedding/js/GLMol.full.js")._repr_javascript_()
